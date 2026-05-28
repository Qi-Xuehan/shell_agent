from utils.llm_helper import LLMHelper
from utils.extract_code import extract_shell_command
from utils.code_executor import execute_shell_command
from utils.session_dir import create_session_dir
from prompts import SYSTEM_PROMPT
from lib.utils import log_info, save_history, show_history, clear_history

class ShellAgent:
    def __init__(self):
        self.llm = LLMHelper()
        self.session_dir = create_session_dir()

    def handle_query(self, query):
        query = query.strip().lower()
        # 纯自然语言意图识别（无数字菜单）
        if any(k in query for k in ["历史", "查看历史", "命令历史"]):
            show_history()
            return
        if any(k in query for k in ["清空历史", "清除记录", "删除历史"]):
            clear_history()
            return
        if any(k in query for k in ["退出", "quit", "exit", "再见"]):
            print("再见！")
            exit(0)

        # 调用DeepSeek V4 Pro生成命令
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ]
        print("正在调用DeepSeek V4 Pro生成命令...")
        response = self.llm.chat(messages)
        cmd = extract_shell_command(response)

        if not cmd:
            print("未能解析到有效命令，请重新描述需求")
            return

        print(f"\n生成命令：{cmd}")
        confirm = input("是否执行？(y/n) ").lower()
        if confirm != "y":
            print("已取消执行")
            return

        # 执行命令
        result = execute_shell_command(cmd)
        if result["success"]:
            print("\n执行结果：")
            print(result["stdout"])
            save_history(query, cmd)
            log_info(f"执行成功：{cmd}")
        else:
            print(f"\n执行失败：{result.get('stderr', result.get('error'))}")
            log_info(f"执行失败：{cmd}")