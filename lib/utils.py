import os
import time
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
HISTORY_DIR = os.path.join(BASE_DIR, "history")

# 初始化目录
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(HISTORY_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "agent.log")
HISTORY_FILE = os.path.join(HISTORY_DIR, "cmd_history.txt")

def log_info(msg):
    t = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{t}] [INFO] {msg}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line)
    print(line.strip())

def save_history(question, cmd):
    t = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"时间:{t} | 需求:{question} | 命令:{cmd}\n"
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(line)

def show_history():
    if not os.path.exists(HISTORY_FILE):
        print("暂无历史记录")
        return
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        print(f.read())

def clear_history():
    open(HISTORY_FILE, "w", encoding="utf-8").close()
    print("历史记录已清空")