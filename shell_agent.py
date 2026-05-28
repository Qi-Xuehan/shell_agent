from utils.llm_helper import LLMHelper
from utils.extract_code import extract_shell_command, extract_json_from_llm
from utils.code_executor import execute_shell_command
from utils.session_dir import create_session_dir
from prompts import SYSTEM_PROMPT, DIAGNOSE_PROMPT
from lib.utils import log_info, save_history, show_history, clear_history

class ShellAgent:
    def __init__(self):
        self.llm = LLMHelper()
        self.session_dir = create_session_dir()

    def handle_query(self, query):
        query = query.strip().lower()

        # 系统指令
        if any(k in query for k in ["退出", "quit", "exit", "再见"]):
            print("再见！")
            exit(0)
        elif any(k in query for k in ["清空历史", "清除记录", "删除历史"]):
            clear_history()
            return
        elif any(k in query for k in ["历史", "查看历史", "命令历史"]):
            show_history()
            return

        # ==============================
        # 统一自动化诊断
        # ==============================
        if any(k in query for k in ["检查", "诊断", "分析", "问题", "状态"]):
            self.auto_diagnose(query)
            return

        # 普通命令生成
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ]
        print("正在调用DeepSeek V4 Pro生成命令...")
        response = self.llm.chat(messages)
        cmd = extract_shell_command(response)

        if not cmd:
            print("未能解析到有效命令")
            return

        print(f"\n生成命令：{cmd}")
        confirm = input("是否执行？(y/n) ").lower()
        if confirm != "y":
            print("已取消执行")
            return

        result = execute_shell_command(cmd)
        if result["success"]:
            print("\n执行结果：")
            print(result["stdout"])
            save_history(query, cmd)
        else:
            print(f"\n执行失败：{result.get('stderr')}")

    # ==============================
    # 自动诊断引擎
    # ==============================
    def auto_diagnose(self, query):
        print("\n→ 正在自动执行诊断...")

        # 1. 让大模型生成：要执行的命令列表 + 分析格式
        messages = [
            {"role": "system", "content": DIAGNOSE_PROMPT},
            {"role": "user", "content": f"请诊断：{query}"}
        ]

        try:
            llm_response = self.llm.chat(messages)
        except Exception as e:
          print(f"诊断失败：调用大模型出错 - {e}")
          print("使用备用诊断方案...")
          self.fallback_diagnose(query)
          return

        # 2. 解析大模型返回的 JSON 格式命令
        diagnose_data = extract_json_from_llm(llm_response)
        if not diagnose_data:
            print("诊断失败：格式错误")
            print("使用备用诊断方案...")
            return

        title = diagnose_data.get("title", "系统诊断")
        commands = diagnose_data.get("commands", [])
        analysis = diagnose_data.get("analysis", "分析完成")

        # 3. 自动执行所有命令
        results = {}
        for cmd in commands:
            print(f"→ 执行：{cmd}")
            res = execute_shell_command(cmd)
            results[cmd] = res["stdout"][:500]  # 截取结果

        # 4. 输出格式化诊断报告
        print("=" * 60)
        print(f"【{title}】")
        print(analysis)
        print("=" * 60)

# 备用诊断方案
    def fallback_diagnose(self, query):
        if "磁盘" in query or "空间" in query:
           print("\n===== 备用磁盘诊断 =====")
           print("→ 执行：df -h")
           print(execute_shell_command("df -h")["stdout"])
           print("\n→ 执行：du -sh /* 2>/dev/null | sort -rh | head -5")
           print(execute_shell_command("du -sh /* 2>/dev/null | sort -rh | head -5")["stdout"])
           print("===== 诊断完成 =====")
        else:
            print("暂时无法自动诊断，请直接输入具体命令生成需求")