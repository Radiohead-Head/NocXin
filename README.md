# Weekly Report CLI

基于 LangChain 和 MCP 协议的命令行周报生成工具。

## 功能特性

- 支持多种数据获取模式：直接 HTTP、Web Agent、MCP 协议
- MCP 协议支持 Basic Auth 和 Bearer Token 认证
- 自动从网页提取关键数据生成结构化 Markdown 周报
- 支持输出到文件或直接打印

## 项目结构

```
/home/langC/NocXin
├── config.py                 # 应用配置
├── requirements.txt          # Python 依赖
├── main.py                   # 主入口
├── cli.py                    # CLI 命令行工具
├── .env.example              # 环境变量示例
├── tools/
│   ├── __init__.py
│   ├── web_tools.py          # HTTP 网页抓取工具
│   ├── mcp_tools.py          # MCP 协议客户端工具
│   └── mcp_server.py         # 本地 MCP 服务器
└── workflows/
    ├── __init__.py
    └── report/               # 周报功能模块
        ├── __init__.py
        ├── chain.py          # 简单 Chain 模式
        ├── agent_chain.py    # Agent 模式
        └── mcp_chain.py      # MCP 模式

# 未来扩展示例：
# workflows/analyze/         # 数据分析模块
# workflows/summary/         # 会议总结模块
```

## 安装

```bash
pip install -r requirements.txt
```

## 配置

复制环境变量示例文件并配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
# ===== LLM 配置 =====
OPENAI_API_KEY=your_api_key_here
OPENAI_API_BASE_URL=https://api.openai.com/v1
MODEL_NAME=gpt-4o-mini

# ===== MCP 服务（可选）=====
MCP_SERVER_COMMAND=python
MCP_SERVER_ARGS=["tools/mcp_server.py"]

# ===== 周报数据源 =====
REPORT_URL=https://example.com/weekly-data
REPORT_USER=""
REPORT_TOKEN=""
```

## 使用方法

### 生成周报

```bash
# 生成周报（使用 .env 中配置的 REPORT_URL）
python main.py report

# 输出到文件
python main.py report --output weekly.md
```

### 工作原理

程序会**自动选择最佳数据源**：

1. **优先使用 MCP 协议**（如果配置了 `MCP_SERVER_COMMAND`）
   - 支持多种认证方式（Basic Auth、Token、Cookie、表单登录）
   - 适合需要认证的内部系统（如 Jira、Confluence）

2. **回退到 HTTP 直接请求**
   - 无需额外配置
   - 适合公开网页

### 帮助信息

```bash
# 查看所有可用命令
python main.py --help

# 查看周报命令帮助
python main.py report --help
```

### 扩展示例

未来可以添加更多功能模块：

```bash
# 数据分析（示例）
python main.py analyze data

# 会议总结（示例）
python main.py summary meeting
```

## 配置说明

| 配置块 | 说明 | 必填 |
|--------|------|------|
| **LLM 配置** | OpenAI API 密钥和模型 | ✅ |
| **周报数据源** | URL + 用户名 + Token | ✅ |
| **MCP 服务** | MCP 服务器启动命令 | 可选 |

MCP 模式下会调用两个工具：
- `fetch_content`: 获取网页全文内容
- `get_page_data`: 获取网页特定数据（支持 CSS 选择器）

## 依赖包

- `langchain>=0.1.0` - LangChain 核心框架
- `langchain-community>=0.0.10` - LangChain 社区组件
- `langchain-core>=0.1.0` - LangChain 核心组件
- `openai>=1.0.0` - OpenAI API 客户端
- `requests>=2.31.0` - HTTP 请求库
- `beautifulsoup4>=4.12.0` - HTML 解析库
- `lxml>=4.9.0` - XML/HTML 解析器
- `python-dotenv>=1.0.0` - 环境变量管理
- `click>=8.1.0` - CLI 框架
- `mcp>=1.0.0` - MCP 协议支持

## 依赖管理

```bash
# 检查可更新的依赖（只查看）
python3 scripts/update_deps.py

# 更新到最新版本
python3 scripts/update_deps.py --write

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: MCP 模式下工具名称不对怎么办？

修改 [tools/mcp_tools.py](file:///home/langC/NocXin/tools/mcp_tools.py) 中的 `call_mcp_tool` 调用：

```python
# 将 "fetch_content" 改为你实际的 MCP 工具名称
result = client.call_mcp_tool("your_tool_name", {"url": url})
```

### Q: 如何添加自定义网页解析逻辑？

在 [tools/web_tools.py](file:///home/langC/forxin/tools/web_tools.py) 或 [tools/mcp_tools.py](file:///home/langC/forxin/tools/mcp_tools.py) 中添加新的工具函数。

### Q: 如何修改周报生成模板？

编辑 [config.py](file:///home/langC/forxin/config.py) 中的 `REPORT_TEMPLATE` 变量，或修改 [chains/weekly_report.py](file:///home/langC/forxin/chains/weekly_report.py) 中的 prompt。
