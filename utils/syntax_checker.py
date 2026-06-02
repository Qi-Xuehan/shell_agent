import subprocess

# 语法检查
def check_bash_syntax(cmd):
    """校验bash命令语法是否合法"""
    try:
        # 仅语法检查，不执行
        res = subprocess.run(
            ["bash", "-n", "-c", cmd],
            capture_output=True,
            text=True
        )
        if res.returncode == 0:
            return True, "语法合法"
        else:
            return False, f"语法错误: {res.stderr.strip()}"
    except Exception as e:
        return False, f"校验异常: {str(e)}"


# 命令安全风险等级判断
def check_command_risk(cmd):
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