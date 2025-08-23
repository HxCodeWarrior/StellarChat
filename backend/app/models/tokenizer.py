from transformers import AutoTokenizer
from app.config import settings
from app.utils import get_logger

logger = get_logger()

class Tokenizer:
    def __init__(self, model_path: str = settings.MODEL_PATH):
        logger.info(f"加载分词器: {model_path}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)

        # 如果分词器需要特殊处理（如添加填充token），可在此添加
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

    def encode(self, text: str):
        return self.tokenizer.encode(text, return_tensors="pt")

    def decode(self, tokens):
        return self.tokenizer.decode(tokens, skip_special_tokens=True)
