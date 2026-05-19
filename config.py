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


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_API_BASE_URL = os.getenv("OPENAI_API_BASE_URL", "")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")

WEB_PAGE_URL = os.getenv("WEB_PAGE_URL", "https://example.com/weekly-data")

MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "")
MCP_AUTH_TYPE = os.getenv("MCP_AUTH_TYPE", "basic")
MCP_USERNAME = os.getenv("MCP_USERNAME", "")
MCP_PASSWORD = os.getenv("MCP_PASSWORD", "")
MCP_TOKEN = os.getenv("MCP_TOKEN", "")

MCP_SERVER_COMMAND = os.getenv("MCP_SERVER_COMMAND", "")
MCP_SERVER_ARGS = parse_env_list(os.getenv("MCP_SERVER_ARGS", ""))
MCP_SERVER_ENV = parse_env_dict(os.getenv("MCP_SERVER_ENV", ""))

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