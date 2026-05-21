import sys
import os

# 把项目根目录加入 Python 路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from lib.utils import log_info, save_history, show_history, clear_history
from lib.llm_agent import nl2bash
from lib.syntax_checker import check_bash_syntax

def main():
    if len(sys.argv) < 2:
        return
    query = sys.argv[1]
    query = query.strip().lower()

    # 意图1：退出
    if any(k in query for k in ["退出", "quit", "exit", "关闭"]):
        sys.exit(99)

    # 意图2：查看历史
    if any(k in query for k in ["历史", "查看历史", "历史记录"]):
        show_history()
        return

    # 意图3：清空历史
    if any(k in query for k in ["清空历史", "删除历史", "清除记录"]):
        clear_history()
        return

    # 意图4：生成 Shell 命令（默认）
    commands, msg = nl2bash(query)
    print(f"→ {msg}")

    if not commands:
        return

    # 取第一个匹配的命令
    cmd_item = commands[0]
    desc = cmd_item["desc"]
    cmd = cmd_item["cmd"]

    print(f"→ 推荐命令：{cmd}")
    print(f"→ 功能说明：{desc}")

    # 语法校验
    ok, reason = check_bash_syntax(cmd)
    print(f"→ 语法校验：{reason}")

    if not ok:
        return

    # 确认执行
    confirm = input("→ 是否执行？(y/n) ").lower()
    if confirm == "y":
        import os
        print("→ 执行结果：")
        os.system(cmd)
        save_history(query, cmd)
        log_info(f"执行命令: {cmd}")

if __name__ == "__main__":
    main()