import os
from dotenv import load_dotenv

load_dotenv()

class LLMConfig:
    # DeepSeek API配置
    API_KEY = os.getenv("DEEPSEEK_API_KEY")
    BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    MODEL_NAME = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    TEMPERATURE = 0.1
    MAX_TOKENS = 1024