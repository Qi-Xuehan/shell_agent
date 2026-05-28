from shell_agent import ShellAgent

def main():
    print("="*60)
    print("        Shell Agent - Shell编程助手        ")
    print("="*60)
    print("支持：自然语言生成命令 / 查看历史 / 清空历史 / 退出")
    print("="*60)

    agent = ShellAgent()
    while True:
        query = input("\n请输入指令 > ")
        if not query.strip():
            continue
        agent.handle_query(query)

if __name__ == "__main__":
    main()