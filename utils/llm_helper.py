from openai import OpenAI
from config.llm_config import LLMConfig

class LLMHelper:
    def __init__(self):
        self.client = OpenAI(
            api_key=LLMConfig.API_KEY,
            base_url=LLMConfig.BASE_URL
        )
        self.model = LLMConfig.MODEL_NAME

    def chat(self, messages):
        """调用DeepSeek V4 Pro，完全对齐你提供的首次调用格式"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=LLMConfig.TEMPERATURE,
            max_tokens=LLMConfig.MAX_TOKENS,
            stream=LLMConfig.STREAM,  # 关闭流式输出
            reasoning_effort=LLMConfig.REASONING_EFFORT,  # 高推理强度
            # 关键：修正 thinking 参数格式（官方标准）
            extra_body={
                "thinking": {
                    "type": "enabled"  # 启用思考模式
                }
            }
        )
        return response.choices[0].message.content.strip()