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

    def encode(self, text: str, **kwargs):
        """编码文本"""
        return self.tokenizer.encode(text, **kwargs)

    def decode(self, tokens, **kwargs):
        """解码token"""
        return self.tokenizer.decode(tokens, **kwargs)

    def tokenize(self, text: str, **kwargs):
        """分词"""
        return self.tokenizer.tokenize(text, **kwargs)