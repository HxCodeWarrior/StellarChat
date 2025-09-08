from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "HuggingFaceTB/SmolLM-135M-Instruct"
print(f"正在下载模型: {model_name}")

# 加载tokenizer和模型
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True)

# 保存到本地目录
save_path = "./backend/models/test/SmolLM-135M-Instruct"
print(f"正在保存模型到: {save_path}")
tokenizer.save_pretrained(save_path)
model.save_pretrained(save_path)

print("模型下载和保存完成!")