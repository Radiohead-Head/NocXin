# NocXin 依赖管理

## 常用命令

```bash
# 检查可更新的依赖（只查看，不修改）
python scripts/update_deps.py

# 更新依赖到最新版本
python scripts/update_deps.py --write

# 安装依赖
pip install -r requirements.txt

# 导出当前环境依赖
pip freeze > requirements.txt
```

## 依赖说明

| 包名 | 用途 |
|------|------|
| langchain | LLM 应用框架 |
| langchain-community | LangChain 社区集成 |
| openai | OpenAI API 客户端 |
| requests | HTTP 请求 |
| beautifulsoup4 | HTML 解析 |
| lxml | XML/HTML 解析器 |
| python-dotenv | 环境变量加载 |
| click | CLI 框架 |
| mcp | MCP 协议支持 |
