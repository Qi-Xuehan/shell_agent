# 修复终端中文输入问题
import sys
import io
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

from utils.llm_helper import LLMHelper
from utils.extract_code import extract_shell_command, extract_json_from_llm
from utils.code_executor import execute_shell_command
from utils.session_dir import create_session_dir
from prompts import SYSTEM_PROMPT, DIAGNOSE_PROMPT
from utils.history import log_info, save_history, show_history, clear_history
from utils.syntax_checker import check_bash_syntax
import os

class ShellAgent:
    def __init__(self):
        self.llm = LLMHelper()
        self.session_dir = create_session_dir()
        self.session_log = os.path.join(self.session_dir, "session.log")

    # 日志写入（自动清洗编码，防止报错）
    def log_to_session(self, content):
        cleaned = content.encode("utf-8", "ignore").decode("utf-8")
        with open(self.session_log, "a", encoding="utf-8") as f:
            f.write(cleaned + "\n")

    # 命令安全风险等级判断
    def check_command_risk(self, cmd):
        dangerous = [
            "rm -rf", "rm -fr", "mkfs", "dd", "shutdown",
            "reboot", "init 0", "poweroff", "halt"
        ]
        warning = [
            "rm", "chmod", "chown", "useradd", "userdel",
            "passwd", "kill", "killall", "umount"
        ]

        for d in dangerous:
            if d in cmd:
                return "危险", "❌ 命令包含高危操作，已禁止执行"

        for w in warning:
            if w in cmd:
                return "警告", "⚠️ 该命令会修改系统/文件权限，请谨慎确认"

        return "安全", "✅ 命令安全，可正常执行"

    # 命令执行结果自动总结
    def summarize_result(self, cmd, output):
        if not output or len(output.strip()) == 0:
            return "命令执行成功，但无返回内容"

        try:
            messages = [
                {"role": "system", "content": """
你是Linux运维助手，用简洁中文总结命令执行结果。
总结包含：执行状态、关键数据、是否异常、简短建议。
不要格式、不要markdown、纯文字。
"""},
                {"role": "user", "content": f"命令：{cmd}\n输出：{output[:2000]}"}
            ]
            res = self.llm.chat(messages)
            return res.encode("utf-8", "ignore").decode("utf-8")
        except:
            return "API超时，总结失败"

    # 获取命令中文解释
    def get_command_explanation(self, cmd):
        try:
            messages = [
                {"role": "system", "content": """
你是一个Linux命令解释专家，用简洁中文解释命令，必须包含3点：
1. 功能
2. 参数含义
3. 使用场景
只返回解释，不要多余内容，不要使用表情符号。
"""},
                {"role": "user", "content": f"解释命令：{cmd}"}
            ]
            res = self.llm.chat(messages)
            return res.encode("utf-8", "ignore").decode("utf-8")
        except:
            return "无法获取解释（API异常）"

    def handle_query(self, query):
        query = query.strip().lower()
        self.log_to_session(f"用户输入：{query}")
        log_info(f"用户输入：{query}")

        # 系统指令
        if any(k in query for k in ["退出", "quit", "exit", "再见"]):
            print("再见！")
            log_info("用户退出程序")
            exit(0)
        elif any(k in query for k in ["清空历史", "清除记录", "删除历史"]):
            clear_history()
            self.log_to_session("操作：清空历史记录")
            log_info("用户执行：清空历史记录")
            return
        elif any(k in query for k in ["历史", "查看历史", "命令历史"]):
            show_history()
            self.log_to_session("操作：查看历史记录")
            log_info("用户执行：查看历史记录")
            return

        # 自动化诊断
        if any(k in query for k in ["检查", "诊断", "分析", "问题", "状态"]):
            self.auto_diagnose(query)
            return

        # 普通命令生成
        print("\n正在生成命令并进行校验...")
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ]

        try:
            response = self.llm.chat(messages)
        except:
            print("大模型调用失败")
            log_info("大模型调用失败")
            return

        cmd = extract_shell_command(response)
        if not cmd:
            print("未能解析到有效命令")
            log_info("未能解析到有效命令")
            return

        # 命令语法校验
        is_valid, msg = check_bash_syntax(cmd)
        print("========================")
        print(f"语法校验：{msg}")
        log_info(f"命令校验结果：{msg}，命令内容：{cmd}")

        if not is_valid:
            print("命令非法，已禁止执行")
            self.log_to_session(f"命令非法：{msg}")
            log_info(f"命令非法，已阻止执行：{cmd}")
            return

        # 风险等级判断
        risk_level, risk_msg = self.check_command_risk(cmd)
        print(f"风险等级：{risk_level} | {risk_msg}")
        self.log_to_session(f"风险等级：{risk_level} | 命令：{cmd}")

        # 危险命令直接拦截
        if risk_level == "危险":
            print("❌ 危险命令，终止执行！")
            log_info(f"已拦截危险命令：{cmd}")
            return

        # 自动生成中文解释
        print("详细说明：")
        explain = self.get_command_explanation(cmd)
        print(explain)
        print("========================")
        print(f"\n最终可执行命令：{cmd}")
        self.log_to_session(f"合法命令：{cmd}\n说明：{explain}")

        confirm = input("是否执行？(y/n) ").lower()
        if confirm != "y":
            print("已取消执行")
            self.log_to_session("用户取消执行")
            log_info(f"用户取消执行命令：{cmd}")
            return

        # 执行
        result = execute_shell_command(cmd)
        if result["success"]:
            print("\n执行结果：")
            print(result["stdout"])
            save_history(query, cmd)
            self.log_to_session("执行成功")
            log_info(f"命令执行成功：{cmd}")


            # 自动总结输出
            print("\n===== 智能总结 =====")
            summary = self.summarize_result(cmd, result["stdout"])
            print(summary)
            self.log_to_session(f"执行总结：{summary}")

        else:
            err = result.get("stderr", "未知错误")
            print(f"\n执行失败：{err}")
            self.log_to_session(f"执行失败：{err}")
            log_info(f"命令执行失败：{cmd}，错误：{err}")

    # 自动诊断引擎
    def auto_diagnose(self, query):
        print("\n→ 正在自动执行诊断...")
        self.log_to_session(f"诊断：{query}")
        log_info(f"开始自动诊断：{query}")

        try:
            messages = [
                {"role": "system", "content": DIAGNOSE_PROMPT},
                {"role": "user", "content": f"请诊断：{query}"}
            ]
            res = self.llm.chat(messages)
            data = extract_json_from_llm(res)
        except:
            print("诊断超时，使用本地备用方案")
            log_info("大模型诊断超时，切换本地备用方案")
            self.fallback_diagnose(query)
            return

        if not data:
            print("解析失败")
            log_info("诊断结果解析失败")
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
            log_info(f"诊断执行命令：{cmd}")

        print("\n========================")
        print(f"【{title}】")
        print(analysis)
        print("========================\n")
        self.log_to_session(f"诊断完成：{title}")
        log_info(f"自动诊断完成：{title}")

    def fallback_diagnose(self, query):
        if "磁盘" in query:
            print("\n本地磁盘诊断：")
            os.system("df -h")
            print("\n占用最大目录：")
            os.system("du -sh /* 2>/dev/null | sort -rh | head -5")
        log_info("备用本地诊断执行完成")