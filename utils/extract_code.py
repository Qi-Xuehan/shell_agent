import re

def extract_shell_command(text):
    """从大模型返回文本中提取Shell命令"""
    pattern = r"```bash\n(.*?)\n```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    # 备用匹配：直接提取单行命令
    pattern2 = r"命令：(.*?)(\n|$)"
    match2 = re.search(pattern2, text)
    if match2:
        return match2.group(1).strip()
    return None