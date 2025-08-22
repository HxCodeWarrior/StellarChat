import os

class Settings:
    PROJECT_NAME: str = "StellarByte LLM Chat Backend"
    VERSION: str = "0.1.0"

    # 模型路径（可以替换成你自己的模型路径）
    MODEL_PATH: str = os.getenv("MODEL_PATH", "./models/llm")
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))

settings = Settings()
