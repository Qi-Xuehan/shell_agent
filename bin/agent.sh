#!/bin/bash
# agent.sh - 终端交互式 Agent

while true; do
    echo "=== Shell指令自动生成Agent ==="
    echo "1. 输入中文需求生成命令"
    echo "2. 查看模板库"
    echo "3. 添加模板"
    echo "4. 查看历史记录"
    echo "5. 退出"
    read -p "请选择操作：" choice

    case $choice in
        1)
            read -p "请输入中文需求：" user_input
            # 模板匹配
            cmd=$(python3 - <<END
from lib.utils import load_templates
templates = load_templates()
print(templates.get("$user_input", "echo '未匹配到模板命令'"))
END
)
            # 校验语法
            valid=$(python3 -c "from lib.syntax_checker import check_syntax; print(check_syntax('$cmd'))")
            echo "生成命令: $cmd"
            if [[ "$valid" == "False" ]]; then
                echo "⚠️ 命令语法不合法"
                continue
            fi
            read -p "是否执行该命令? (y/n)：" confirm
            if [[ "$confirm" == "y" ]]; then
                eval "$cmd"
            fi
            python3 - <<END
from lib.utils import save_log, save_history
save_log("执行命令: $cmd")
save_history("$cmd")
END
            ;;
        2)
            python3 - <<END
from lib.utils import list_templates
list_templates()
END
            ;;
        3)
            read -p "输入模板名称：" t_name
            read -p "输入模板命令：" t_cmd
            python3 - <<END
from lib.utils import add_template
add_template("$t_name", "$t_cmd")
END
            echo "模板已添加"
            ;;
        4)
            cat ../history/history.txt
            ;;
        5)
            echo "退出 Agent"
            break
            ;;
        *)
            echo "无效选择"
            ;;
    esac
done