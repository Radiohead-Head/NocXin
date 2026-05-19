import os
import json
from typing import Optional, List, Dict
from dotenv import load_dotenv

load_dotenv()


def parse_env_list(value: str) -> List[str]:
    if not value:
        return []
    try:
        return json.loads(value)
    except:
        return [item.strip() for item in value.split(",") if item.strip()]


def parse_env_dict(value: str) -> Dict[str, str]:
    if not value:
        return {}
    try:
        return json.loads(value)
    except:
        return {}


# ===== LLM 配置 =====
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_API_BASE_URL = os.getenv("OPENAI_API_BASE_URL", "")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")

# ===== MCP 服务配置 =====
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "")
MCP_SERVER_COMMAND = os.getenv("MCP_SERVER_COMMAND", "")
MCP_SERVER_ARGS = parse_env_list(os.getenv("MCP_SERVER_ARGS", ""))
MCP_SERVER_ENV = parse_env_dict(os.getenv("MCP_SERVER_ENV", ""))

# ===== 周报数据源 =====
REPORT_URL = os.getenv("REPORT_URL", "https://example.com/weekly-data")
REPORT_USER = os.getenv("REPORT_USER", "")
REPORT_TOKEN = os.getenv("REPORT_TOKEN", "")

REPORT_TEMPLATE = """## 周报总结

### 本周工作概览
{overview}

### 关键数据
{key_data}

### 下周计划
{next_week_plan}

### 需要关注的问题
{issues}
"""