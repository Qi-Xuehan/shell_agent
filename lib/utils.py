import os
import json
from datetime import datetime

HISTORY_FILE = "../history/history.txt"
LOG_FILE = "../logs/agent.log"
TEMPLATE_FILE = "../config/templates.json"

# 日志
def save_log(msg: str):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} | {msg}\n")

# 历史
def save_history(cmd: str):
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} | {cmd}\n")

# 模板管理
def load_templates() -> dict:
    if not os.path.exists(TEMPLATE_FILE):
        return {}
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def add_template(name: str, cmd: str):
    templates = load_templates()
    templates[name] = cmd
    with open(TEMPLATE_FILE, "w", encoding="utf-8") as f:
        json.dump(templates, f, indent=4, ensure_ascii=False)

def list_templates():
    templates = load_templates()
    for i, (name, cmd) in enumerate(templates.items(), 1):
        print(f"{i}. {name} → {cmd}")