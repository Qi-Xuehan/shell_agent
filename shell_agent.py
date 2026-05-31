from utils.llm_helper import LLMHelper
from utils.extract_code import extract_shell_command, extract_json_from_llm
from utils.code_executor import execute_shell_command
from utils.session_dir import create_session_dir
from prompts import SYSTEM_PROMPT, DIAGNOSE_PROMPT
from lib.utils import log_info, save_history, show_history, clear_history
from lib.syntax_checker import check_bash_syntax  # 语法校验

import os

class ShellAgent:
    def __init__(self):
        self.llm = LLMHelper()
        self.session_dir = create_session_dir()
        self.session_log = os.path.join(self.session_dir, "session.log")

    def log_to_session(self, content):
        with open(self.session_log, "a", encoding="utf-8") as f:
            f.write(content + "\n")

    def handle_query(self, query):
        query = query.strip().lower()
        self.log_to_session(f"用户输入：{query}")

        # 系统指令
        if any(k in query for k in ["退出", "quit", "exit", "再见"]):
            print("再见！")
            exit(0)
        elif any(k in query for k in ["清空历史", "清除记录", "删除历史"]):
            clear_history()
            self.log_to_session("操作：清空历史记录")
            return
        elif any(k in query for k in ["历史", "查看历史", "命令历史"]):
            show_history()
            self.log_to_session("操作：查看历史记录")
            return

        # 自动化诊断
        if any(k in query for k in ["检查", "诊断", "分析", "问题", "状态"]):
            self.auto_diagnose(query)
            return

        # ==============================
        # 普通命令生成
        # ==============================
        print("\n正在生成命令并进行校验...")
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ]

        try:
            response = self.llm.chat(messages)
        except:
            print("大模型调用失败")
            return

        cmd = extract_shell_command(response)
        if not cmd:
            print("未能解析到有效命令")
            return

        # 命令语法校验
        is_valid, msg = check_bash_syntax(cmd)
        print("========================")
        print(f"命令语法校验：{msg}")
        if not is_valid:
            print("命令非法，已禁止执行")
            self.log_to_session(f"命令非法：{msg}")
            return


        # 自动生成中文解释
        print("命令详细说明：")
        explain = self.get_command_explanation(cmd)
        print(explain)
        print("========================")
        print(f"\n最终可执行命令：{cmd}")
        self.log_to_session(f"合法命令：{cmd}\n说明：{explain}")

        confirm = input("是否执行？(y/n) ").lower()
        if confirm != "y":
            print("已取消执行")
            return

        # 执行
        result = execute_shell_command(cmd)
        if result["success"]:
            print("\n执行结果：")
            print(result["stdout"])
            save_history(query, cmd)
            self.log_to_session("执行成功")
        else:
            print(f"\n执行失败：{result.get('stderr')}")
            self.log_to_session("执行失败")

    # 获取命令中文解释
    def get_command_explanation(self, cmd):
        try:
            messages = [
                {"role": "system", "content": """
你是一个Linux命令解释专家，用简洁中文解释命令，必须包含3点：
1. 功能
2. 参数含义
3. 使用场景
只返回解释，不要多余内容。
"""},
                {"role": "user", "content": f"解释命令：{cmd}"}
            ]
            return self.llm.chat(messages)
        except:
            return "无法获取解释（API异常）"


    # 自动诊断引擎
    def auto_diagnose(self, query):
        print("\n→ 正在自动执行诊断...")
        self.log_to_session(f"诊断：{query}")

        try:
            messages = [
                {"role": "system", "content": DIAGNOSE_PROMPT},
                {"role": "user", "content": f"请诊断：{query}"}
            ]
            res = self.llm.chat(messages)
            data = extract_json_from_llm(res)
        except:
            print("诊断超时，使用本地备用方案")
            self.fallback_diagnose(query)
            return

        if not data:
            print("解析失败")
            self.fallback_diagnose(query)
            return

        title = data.get("title", "诊断")
        commands = data.get("commands", [])
        analysis = data.get("analysis", "")

        for cmd in commands:
            print(f"→ 执行：{cmd}")
            ret = execute_shell_command(cmd)
            if ret["success"]:
                print(ret["stdout"])

        print("\n========================")
        print(f"【{title}】")
        print(analysis)
        print("========================\n")
        self.log_to_session(f"诊断完成：{title}")

    def fallback_diagnose(self, query):
        if "磁盘" in query:
            print("\n本地磁盘诊断：")
            os.system("df -h")
            print("\n占用最大目录：")
            os.system("du -sh /* 2>/dev/null | sort -rh | head -5")

# EOF