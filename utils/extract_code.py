import re
import json

def extract_shell_command(text):
    pattern = r"```bash\n(.*?)\n```"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else None

def extract_json_from_llm(text):
    # 直接解析 JSON
    try:
        return json.loads(text.strip())
    except:
        pass
    # 从文本中提取 JSON 片段
    pattern = r"\{.*\}"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except:
            return None
    return None