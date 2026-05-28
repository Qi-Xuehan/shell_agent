# Shell Agent 智能命令助手

---

# 一、项目介绍
Shell Agent 是一款**基于 DeepSeek 大模型**的 Linux 智能命令助手，支持用户通过**纯自然语言对话**生成、校验、执行 Shell 命令。
无需记忆复杂的 Linux 指令，只需输入中文需求，即可自动完成命令生成、语法检查、安全执行、历史记录等功能。

**核心定位**：自然语言 → Linux 命令 → 安全执行 → 日志记录

---

# 二、项目结构
```
shell_agent/
├── .env                # 大模型 API 配置文件
├── main.py             # 项目主入口
├── requirements.txt    # 依赖包列表
├── config/             # 配置模块
│   └── llm_config.py   # LLM 配置
├── utils/              # 工具模块
│   ├── llm_helper.py   # 大模型调用
│   ├── code_executor.py # 命令执行器
│   ├── extract_code.py # 命令提取
│   └── session_dir.py  # 会话管理
├── lib/                # 基础功能库
│   ├── utils.py        # 日志、历史记录
│   └── syntax_checker.py # 语法校验
├── prompts.py          # 系统提示词
├── logs/               # 运行日志
├── history/            # 命令历史
└── outputs/            # 会话输出目录
```

---

# 三、项目功能
✅ **纯自然语言交互**：无菜单、无数字选择，直接对话式使用  
✅ **DeepSeek 大模型集成**：智能生成标准、安全的 Bash 命令  
✅ **命令语法校验**：执行前自动检查命令是否合法  
✅ **安全命令执行**：带超时、异常捕获，防止危险操作  
✅ **历史记录管理**：查看历史、清空历史（自然语言触发）  
✅ **日志自动记录**：所有操作自动写入日志文件  
✅ **会话隔离**：每次运行独立会话目录，便于追溯  

支持自然语言指令示例：
- 查看当前目录文件
- 查看磁盘占用
- 查看进程
- 查看历史记录
- 清空历史
- 退出

---

# 四、使用流程

## 1. 安装系统依赖（Ubuntu）
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
```

## 2. 创建并进入项目目录
```bash
mkdir -p ~/shell_agent
cd ~/shell_agent
```

## 3. 创建并激活虚拟环境（推荐）
```bash
python3 -m venv venv
source venv/bin/activate
```
激活成功后，终端前面会显示 `(venv)`

## 4. 安装 Python 依赖
```bash
pip install openai python-dotenv
```

## 5. 配置 .env 环境变量
```bash
nano .env
```

写入以下内容（**替换成你的 API Key**）：
```
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-v4-pro
```

保存退出：
`Ctrl + O` → 回车 → `Ctrl + X`

## 6. 启动项目
```bash
python3 main.py
```

---

# 五、使用示例


---

# 六、退出虚拟环境
```bash
deactivate
```

