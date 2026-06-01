# Shell Agent 智能命令助手

---

## 一、项目介绍

Shell Agent 是一款**基于 DeepSeek 大模型**的 Linux 智能命令助手，支持用户通过**纯自然语言对话**实现命令生成、语法校验、安全执行、历史管理、全自动系统诊断等一体化能力。
无需记忆复杂的 Linux 指令，输入中文即可完成：命令生成 → 语法检查 → 执行 → 分析 → 日志记录 → 诊断报告。

**核心定位**：自然语言 → Linux 命令 → 安全执行 → 系统诊断 → 会话记录 → 自动化分析

---

## 二、项目结构

```
shell_agent/
├── .env                  # 大模型 API 配置文件
├── main.py               # 项目主入口
├── requirements.txt      # 依赖包列表
├── bin/
│   └── start.sh          # 一键激活虚拟环境并启动项目
├── config/               # 配置模块
│   └── llm_config.py     # LLM 相关配置
├── utils/                # 工具模块
│   ├── llm_helper.py     # 大模型调用封装
│   ├── code_executor.py  # Shell 命令安全执行器
│   ├── extract_code.py   # 命令、JSON 内容提取解析
│   ├── session_dir.py    # 独立会话目录管理
│   ├── history.py        # 运行日志、命令历史管理
│   └── syntax_checker.py # Shell 命令语法校验
├── prompts.py            # 全局提示词（统一交互格式规范）
├── logs/                 # 日志与历史文件存储目录
│   ├── agent.log         # 系统全局运行日志
│   └── cmd_history.txt   # 执行命令历史记录
└── outputs/              # 会话输出根目录
    └── session_xxxx/     # 单次独立会话目录，存放会话日志、诊断记录
```

---

## 三、项目功能

- **纯自然语言交互**：无菜单、无数字选项，全程对话式操作
- **DeepSeek 大模型驱动**：智能生成安全、标准的 Bash 命令
- **命令语法校验**：执行前自动检测语法错误、非法参数
- **安全命令执行**：内置超时、异常捕获，规避高危操作
- **历史记录管理**：支持查看历史、一键清空历史，自然语言触发
- **全自动系统诊断**：一键诊断磁盘、内存、CPU、网络、系统日志等问题
- **统一 Prompt 规范**：依靠提示词定义交互格式，新增诊断场景无需改写底层代码
- **会话隔离记录**：每次运行自动生成独立会话目录，完整留存操作轨迹
- **异常容错机制**：大模型 API 不可用时，自动切换本地备用诊断方案
- **日志持久化**：全局系统日志、命令历史、独立会话日志三层记录，数据完整留存

### 支持自然语言指令示例

- 查看当前目录文件
- 查看磁盘占用
- 读取文件内容
- 处理文本文件
- 检查磁盘空间问题
- 检查内存问题
- 检查 CPU 负载
- 查看历史记录
- 清空历史
- 退出

---

## 四、使用流程

### 环境说明

本项目基于 **Ubuntu Linux** 开发运行，需提前安装 Python 相关环境。

### 1. 安装系统依赖（仅首次执行）

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
```

### 2. 进入项目根目录

将所有项目文件放置到 `shell_agent` 文件夹中，执行以下命令进入目录：

```bash
cd ~/shell_agent
```

### 3. 配置大模型密钥（必须配置，仅首次执行）

编辑环境配置文件，填入你的 DeepSeek API 信息：

```bash
nano .env
```

粘贴以下内容，并替换为你自己的 API Key：

```
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-v4-pro
```

保存并退出编辑器：`Ctrl + O` → 回车 → `Ctrl + X`

### 4. 项目启动方式

提供**一键启动**和**手动启动**两种方式，推荐使用一键启动。

#### 方式一：一键启动（推荐）

##### ① 赋予启动脚本执行权限（仅首次执行）

```bash
chmod +x bin/start.sh
```

##### ② 日常启动项目（每次运行只需执行此行）

```bash
./bin/start.sh
```

脚本自动完成：切换项目目录 → 激活虚拟环境 → 启动主程序。

#### 方式二：手动启动（适合调试、了解运行流程）

##### ① 创建并激活虚拟环境（创建仅首次，激活每次运行都需要）

```bash
# 创建虚拟环境（仅首次）
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate
```

激活成功后，终端前缀会显示 `(venv)`。

##### ② 安装 Python 依赖包（仅首次/依赖更新时执行）

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

##### ③ 运行主程序

```bash
python3 main.py
```

### 5. 退出项目与虚拟环境

1. 在程序交互界面输入 `退出`，即可关闭程序
2. 如需退出虚拟环境，执行命令：

```bash
deactivate
```

---

## 五、使用示例

### 1. 输入自然语言指令——查看磁盘空间

<img src="images/查看磁盘空间.png" width="500" alt="演示图片">

### 2. 输入自然语言指令——查看进程

<img src="images/查看进程.png" width="500" alt="演示图片">

### 3. 输入自然语言指令——检查磁盘空间问题

<img src="images/检查磁盘空间问题.png" width="500" alt="演示图片">

### 4. 输入自然语言指令——检查网络问题

<img src="images/检查网络问题1.png" width="500" alt="演示图片">
<img src="images/检查网络问题2.png" width="500" alt="演示图片">

### 5. 查看并清空历史记录

<img src="images/查看、清空历史.png" width="500" alt="演示图片">

---

## 六、常见问题说明

1. **提示权限不足**
   执行一键启动脚本前，务必运行 `chmod +x bin/start.sh`，该操作仅需执行一次。

2. **依赖安装失败**
   检查网络状态，可先升级 pip：`pip install --upgrade pip`，再重新执行依赖安装命令。

3. **大模型调用报错**
   检查项目根目录下 `.env` 文件，确认 API Key、接口地址、模型名称填写正确。

4. **日志写入编码报错**
   项目已内置特殊字符过滤逻辑，若仍出现异常，检查提示词、输入内容是否包含特殊符号、表情。

5. **找不到配置/日志文件**
   确保执行命令时，当前工作目录为项目根目录 `shell_agent`。
