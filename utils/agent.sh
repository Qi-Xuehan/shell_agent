#!/bin/bash
BASE_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
PYTHON=python3

clear
echo "============================================="
echo "        Shell Agent - 自然语言命令助手        "
echo "============================================="
echo "支持：生成命令 / 查看历史 / 清空历史 / 退出"
echo "============================================="

# 无限循环自然语言输入
while true; do
    read -p "请输入指令 > " query

    # 空输入跳过
    if [ -z "$query" ]; then
        continue
    fi

    # 交给 Python 统一处理所有意图
    $PYTHON "$BASE_DIR/lib/agent_core.py" "$query"

    # 获取退出标记
    exit_code=$?
    if [ $exit_code -eq 99 ]; then
        echo "再见！"
        exit 0
    fi

    echo ""
done