import torch
from transformers import AutoModelForCausalLM
from app.config import settings
from app.utils import get_logger
from app.models.tokenizer import Tokenizer

logger = get_logger()

class LLMInference:
    def __init__(self, model_path: str = settings.MODEL_PATH):
        logger.info(f"加载模型: {model_path}")
        self.tokenizer = Tokenizer(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path, 
            torch_dtype=torch.float16, 
            device_map="auto"  # 自动分配到GPU/CPU
        )
        self.model.eval()

    def chat(self, prompt: str, max_new_tokens: int = 200) -> str:
        inputs = self.tokenizer.encode(prompt)
        outputs = self.model.generate(
            inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.7,
            top_p=0.9
        )
        return self.tokenizer.decode(outputs[0])
    
    def stream_chat(self, prompt: str, max_new_tokens: int = 200):
        """流式逐步生成（逐token输出）"""
        inputs = self.tokenizer.encode(prompt)
        input_ids = inputs.to(self.model.device)

        # 使用 `generate` + `stopping_criteria` 实现逐步生成
        output_ids = input_ids.clone()
        past_key_values = None

        for _ in range(max_new_tokens):
            with torch.no_grad():
                outputs = self.model(
                    output_ids,
                    past_key_values=past_key_values,
                    use_cache=True
                )
                logits = outputs.logits[:, -1, :]
                past_key_values = outputs.past_key_values

                next_token_id = torch.argmax(logits, dim=-1, keepdim=True)
                output_ids = torch.cat([output_ids, next_token_id], dim=-1)

                token = self.tokenizer.decode(next_token_id[0])
                yield token  # 每次返回一个token
