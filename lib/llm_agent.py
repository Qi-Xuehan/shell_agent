# !/usr/bin/env python3
# llm_agent.py - 使用 OpenAI SDK 调用 DeepSeek

import os
from openai import OpenAI

# 初始化客户端
client = OpenAI(
    api_key=os.environ.get("sk-041f83e0510c458e9013210aed8a399c"),  # 环境变量存储 API Key
    base_url="https://api.deepseek.com"
)


def generate_shell_command(nl_text: str) -> str:
    """
    使用 DeepSeek 将中文自然语言解析为 Bash 命令
    """
    messages = [
        {"role": "system", "content": "你是一个Linux运维专家，输出安全标准的Bash命令"},
        {"role": "user", "content": nl_text},
    ]

    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=messages,
        stream=False,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}}
    )

    # 返回生成的命令文本
    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    import sys

    text = sys.argv[1] if len(sys.argv) > 1 else ""
    cmd = generate_shell_command(text)
    print(cmd)