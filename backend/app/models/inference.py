import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from app.config import settings
from app.utils import get_logger
import time

logger = get_logger()


class LLMInference:
    _instance = None
    _initialized = False

    def __new__(cls, model_path: str = settings.MODEL_PATH):
        if cls._instance is None:
            cls._instance = super(LLMInference, cls).__new__(cls)
        return cls._instance

    def __init__(self, model_path: str = settings.MODEL_PATH):
        if not self._initialized:
            logger.info(f"正在加载模型: {model_path}")
            self.model_path = model_path
            self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
            
            # 如果分词器没有pad_token，使用eos_token作为pad_token
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # 加载模型
            self.model = AutoModelForCausalLM.from_pretrained(
                model_path,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto" if torch.cuda.is_available() else None,
                trust_remote_code=True
            )
            self.model.eval()
            self._initialized = True
            logger.info("模型加载完成")

    def format_prompt(self, messages):
        """格式化聊天消息为模型输入格式"""
        prompt = ""
        for message in messages:
            content = ""
            if isinstance(message.content, str):
                content = message.content
            else:
                # 处理多模态内容
                for item in message.content:
                    if item.type == "text" and item.text:
                        content += item.text
            
            if message.role == "user":
                prompt += f"User: {content}\n"
            elif message.role == "assistant":
                prompt += f"Assistant: {content}\n"
        prompt += "Assistant:"
        return prompt

    def chat(self, messages, max_new_tokens: int = 200, temperature: float = 0.7, top_p: float = 1.0):
        """生成完整回复"""
        # 格式化提示词
        prompt = self.format_prompt(messages)
        
        # 编码输入
        inputs = self.tokenizer(prompt, return_tensors="pt", padding=True, truncation=True, add_special_tokens=False)
        # 显式创建attention_mask以避免警告
        if self.tokenizer.pad_token_id == self.tokenizer.eos_token_id:
            attention_mask = (inputs['input_ids'] != self.tokenizer.pad_token_id).long()
            inputs['attention_mask'] = attention_mask
        inputs = {k: v.to(self.model.device) for k, v in inputs.items()}
        
        # 生成回复
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                top_p=top_p,
                do_sample=True,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id
            )
        
        # 解码输出
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # 提取助手回复部分
        response = generated_text[len(prompt):].strip()
        return response

    async def stream_chat(self, messages, max_new_tokens: int = 200, temperature: float = 0.7, top_p: float = 1.0):
        """流式生成回复（逐token输出）"""
        # 格式化提示词
        prompt = self.format_prompt(messages)
        
        # 编码输入
        inputs = self.tokenizer(prompt, return_tensors="pt", padding=True, truncation=True, add_special_tokens=False)
        # 显式创建attention_mask以避免警告
        if self.tokenizer.pad_token_id == self.tokenizer.eos_token_id:
            attention_mask = (inputs['input_ids'] != self.tokenizer.pad_token_id).long()
            inputs['attention_mask'] = attention_mask
        input_ids = inputs.input_ids.to(self.model.device)
        attention_mask = inputs.attention_mask.to(self.model.device) if 'attention_mask' in inputs else None
        
        # 使用模型的generate方法实现流式输出
        with torch.no_grad():
            # 生成回复
            generate_kwargs = {
                "input_ids": input_ids,
                "max_new_tokens": max_new_tokens,
                "temperature": temperature,
                "top_p": top_p,
                "do_sample": True,
                "pad_token_id": self.tokenizer.pad_token_id,
                "eos_token_id": self.tokenizer.eos_token_id,
                "output_scores": True,
                "return_dict_in_generate": True
            }
            
            # 只有当attention_mask存在且不为None时才添加
            if attention_mask is not None:
                generate_kwargs["attention_mask"] = attention_mask
                
            outputs = self.model.generate(**generate_kwargs)
        
        # 解码输出
        generated_tokens = outputs.sequences[0][len(input_ids[0]):]
        
        # 逐token返回
        for token_id in generated_tokens:
            token = self.tokenizer.decode([token_id], skip_special_tokens=True)
            yield token
            
            # 检查是否是结束符
            if token_id == self.tokenizer.eos_token_id:
                break