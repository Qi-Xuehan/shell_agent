import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(BASE_DIR, "config", "templates.json")

# 加载模板
with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
    TEMPLATES = json.load(f)

def nl2bash(user_input):
    """中文自然语言 -> 匹配Shell命令+解释"""
    user_input = user_input.lower()
    matched = []

    # 关键词映射
    keyword_map = {
        "文件": "文件管理",
        "磁盘|占用|空间": "磁盘监控",
        "进程|杀进程|pid": "进程管理",
        "日志|错误|查看日志": "日志分析",
        "权限|chmod|chown": "权限管理",
        "网络|ping|网卡": "网络命令"
    }

    # 匹配分类
    cat = None
    for kwds, c in keyword_map.items():
        for k in kwds.split("|"):
            if k in user_input:
                cat = c
                break
        if cat:
            break

    if not cat:
        return None, "未匹配到常用运维场景，请换描述：文件/磁盘/进程/日志/权限/网络"

    # 返回该分类下所有命令
    return TEMPLATES[cat], f"已匹配【{cat}】分类命令"

def explain_cmd(cmd_desc, cmd):
    """命令解释"""
    return f"""
功能描述：{cmd_desc}
执行命令：{cmd}
使用说明：直接在终端复制执行即可，注意目录和权限
"""