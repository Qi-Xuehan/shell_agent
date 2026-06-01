import os
from dotenv import load_dotenv

load_dotenv()

class LLMConfig:
    # DeepSeek V4 Pro 配置（与你提供的调用完全一致）
    API_KEY = os.getenv("DEEPSEEK_API_KEY")
    BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    MODEL_NAME = os.getenv("DEEPSEEK_MODEL", "deepseek-v4-pro")  # 改为 v4-pro
    TEMPERATURE = 0.1
    MAX_TOKENS = 2048
    # 新增思考模式配置
    REASONING_EFFORT = "high"  # 高推理强度
    STREAM = False  # 关闭流式输出