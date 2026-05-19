import subprocess
import json
import base64
import os
import shlex
from typing import Optional, List
from langchain_core.tools import tool
from config import (
    MCP_SERVER_COMMAND, MCP_SERVER_ARGS, MCP_SERVER_ENV,
    MCP_SERVER_URL, MCP_AUTH_TYPE, MCP_USERNAME, MCP_PASSWORD, MCP_TOKEN
)


class MCPClient:
    def __init__(
        self,
        server_command: Optional[str] = None,
        server_args: Optional[List[str]] = None,
        server_env: Optional[dict] = None,
        server_url: Optional[str] = None,
        auth_type: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        token: Optional[str] = None
    ):
        self.server_command = server_command or MCP_SERVER_COMMAND
        self.server_args = server_args or MCP_SERVER_ARGS or []
        self.server_env = server_env or MCP_SERVER_ENV or {}
        self.server_url = server_url or MCP_SERVER_URL
        self.auth_type = auth_type or MCP_AUTH_TYPE or "none"
        self.username = username or MCP_USERNAME
        self.password = password or MCP_PASSWORD
        self.token = token or MCP_TOKEN

    def call_mcp_tool(self, tool_name: str, arguments: dict) -> str:
        if self.server_command:
            return self._call_via_stdio(tool_name, arguments)
        elif self.server_url:
            return self._call_via_http(tool_name, arguments)
        else:
            raise ValueError("MCP server not configured. Set MCP_SERVER_COMMAND or MCP_SERVER_URL")

    def _get_auth_headers(self) -> dict:
        if self.auth_type == "basic" and self.username:
            credentials = f"{self.username}:{self.password or ''}"
            encoded = base64.b64encode(credentials.encode()).decode()
            return {"Authorization": f"Basic {encoded}"}
        elif self.auth_type == "bearer" and self.token:
            return {"Authorization": f"Bearer {self.token}"}
        return {}

    def _call_via_stdio(self, tool_name: str, arguments: dict) -> str:
        try:
            cmd = [self.server_command] + self.server_args

            env = os.environ.copy()
            env.update(self.server_env)

            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=env
            )

            request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": arguments
                }
            }

            stdout, stderr = process.communicate(
                input=json.dumps(request),
                timeout=30
            )

            if stderr:
                return f"Error: {stderr}"

            response = json.loads(stdout)
            if "result" in response:
                return json.dumps(response["result"], ensure_ascii=False)
            elif "error" in response:
                return f"MCP Error: {response['error']}"
            return stdout

        except subprocess.TimeoutExpired:
            return "Error: MCP request timeout"
        except Exception as e:
            return f"Error calling MCP tool: {str(e)}"

    def _call_via_http(self, tool_name: str, arguments: dict) -> str:
        import requests
        try:
            headers = {"Content-Type": "application/json"}
            headers.update(self._get_auth_headers())

            response = requests.post(
                self.server_url,
                json={
                    "method": "tools/call",
                    "params": {
                        "name": tool_name,
                        "arguments": arguments
                    }
                },
                headers=headers,
                timeout=30
            )
            result = response.json()
            if "result" in result:
                return json.dumps(result["result"], ensure_ascii=False)
            elif "error" in result:
                return f"MCP Error: {result['error']}"
            return response.text
        except Exception as e:
            return f"Error calling MCP tool: {str(e)}"


_mcp_client: Optional[MCPClient] = None


def get_mcp_client() -> MCPClient:
    global _mcp_client
    if _mcp_client is None:
        _mcp_client = MCPClient()
    return _mcp_client


@tool
def mcp_fetch_web_content(url: str) -> str:
    """通过 MCP 协议获取指定网页的文本内容。

    Args:
        url: 要抓取的网页URL

    Returns:
        网页的文本内容，如果失败则返回错误信息
    """
    client = get_mcp_client()
    try:
        result = client.call_mcp_tool("fetch_content", {"url": url})
        return result
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def mcp_get_page_data(url: str, selector: Optional[str] = None) -> str:
    """通过 MCP 协议获取网页数据，支持 CSS 选择器。

    Args:
        url: 要抓取的网页URL
        selector: 可选的 CSS 选择器

    Returns:
        网页数据，如果失败则返回错误信息
    """
    client = get_mcp_client()
    try:
        args = {"url": url}
        if selector:
            args["selector"] = selector
        result = client.call_mcp_tool("get_page_data", args)
        return result
    except Exception as e:
        return f"Error: {str(e)}"