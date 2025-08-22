from transformers import AutoTokenizer
from app.config import settings
from app.utils import get_logger

logger = get_logger()

class Tokenizer:
    def __init__(self, model_path: str = settings.MODEL_PATH):
        logger.info(f"加载分词器: {model_path}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)

    def encode(self, text: str):
        return self.tokenizer.encode(text, return_tensors="pt")

    def decode(self, tokens):
        return self.tokenizer.decode(tokens, skip_special_tokens=True)
