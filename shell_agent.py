from utils.llm_helper import LLMHelper
from utils.extract_code import extract_shell_command, extract_json_from_llm
from utils.code_executor import execute_shell_command
from utils.session_dir import create_session_dir
from prompts import SYSTEM_PROMPT, DIAGNOSE_PROMPT
from lib.utils import log_info, save_history, show_history, clear_history

import os

class ShellAgent:
    def __init__(self):
        self.llm = LLMHelper()
        self.session_dir = create_session_dir()
        # 创建会话日志文件
        self.session_log = os.path.join(self.session_dir, "session.log")

    def log_to_session(self, content):
        """写入会话日志"""
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

        # 普通命令生成
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ]
        print("正在调用DeepSeek V4 Pro生成命令...")
        self.log_to_session("调用大模型生成命令...")
        response = self.llm.chat(messages)
        cmd = extract_shell_command(response)

        if not cmd:
            print("未能解析到有效命令")
            self.log_to_session("错误：未能解析到有效命令")
            return

        print(f"\n生成命令：{cmd}")
        self.log_to_session(f"生成命令：{cmd}")
        confirm = input("是否执行？(y/n) ").lower()
        if confirm != "y":
            print("已取消执行")
            self.log_to_session("用户取消执行")
            return

        result = execute_shell_command(cmd)
        if result["success"]:
            print("\n执行结果：")
            print(result["stdout"])
            self.log_to_session(f"执行成功，结果：\n{result['stdout']}")
            save_history(query, cmd)
        else:
            print(f"\n执行失败：{result.get('stderr')}")
            self.log_to_session(f"执行失败：{result.get('stderr')}")

    def auto_diagnose(self, query):
        print("\n→ 正在自动执行诊断...")
        self.log_to_session(f"开始自动诊断：{query}")

        # 1. 调用大模型生成诊断指令
        messages = [
            {"role": "system", "content": DIAGNOSE_PROMPT},
            {"role": "user", "content": f"请诊断：{query}"}
        ]

        try:
            llm_response = self.llm.chat(messages)
            self.log_to_session(f"大模型返回：{llm_response}")
        except Exception as e:
            print(f"诊断失败：调用大模型出错 - {e}")
            self.log_to_session(f"诊断失败：{e}")
            self.fallback_diagnose(query)
            return

        # 2. 解析 JSON
        diagnose_data = extract_json_from_llm(llm_response)
        if not diagnose_data:
            print("诊断失败：无法解析大模型返回的格式")
            self.log_to_session("解析大模型返回格式失败")
            self.fallback_diagnose(query)
            return

        title = diagnose_data.get("title", "系统诊断")
        commands = diagnose_data.get("commands", [])
        analysis = diagnose_data.get("analysis", "分析完成")

        # 3. 执行命令并记录结果
        results = {}
        for cmd in commands:
            print(f"→ 执行：{cmd}")
            res = execute_shell_command(cmd)
            results[cmd] = res["stdout"]
            self.log_to_session(f"执行命令：{cmd}\n结果：{res['stdout']}")

        # 4. 输出并写入诊断报告
        report = f"""
============================================
【{title}】
{analysis}
============================================
"""
        print(report)
        self.log_to_session(report)

    def fallback_diagnose(self, query):
        if "磁盘" in query or "空间" in query:
            print("\n===== 备用磁盘诊断 =====")
            cmds = ["df -h", "du -sh /* 2>/dev/null | sort -rh | head -5"]
            for cmd in cmds:
                print(f"→ 执行：{cmd}")
                res = execute_shell_command(cmd)["stdout"]
                print(res)
                self.log_to_session(f"备用诊断命令：{cmd}\n结果：{res}")
            print("===== 诊断完成 =====")
            self.log_to_session("备用磁盘诊断完成")
        else:
            print("暂时无法自动诊断，请直接输入具体命令生成需求")
            self.log_to_session("无对应备用诊断方案")