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
        """调用大模型对话接口"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=LLMConfig.TEMPERATURE,
            max_tokens=LLMConfig.MAX_TOKENS
        )
        return response.choices[0].message.content.strip()