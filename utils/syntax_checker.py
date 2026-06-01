import subprocess

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