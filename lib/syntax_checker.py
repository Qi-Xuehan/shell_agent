import subprocess

def check_syntax(cmd: str) -> bool:
    """
    使用 bash -n 检查命令语法合法性，不执行
    """
    try:
        subprocess.run(['bash', '-n', '-c', cmd], check=True)
        return True
    except subprocess.CalledProcessError:
        return False