from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import requests
from bs4 import BeautifulSoup
from typing import Any
import os
import asyncio

server = Server("weekly-report-mcp")

REPORT_USER = os.getenv("REPORT_USER", "")
REPORT_TOKEN = os.getenv("REPORT_TOKEN", "")


def _get_session():
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    })

    if REPORT_USER and REPORT_TOKEN:
        session.auth = (REPORT_USER, REPORT_TOKEN)

    return session


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="fetch_content",
            description="获取指定网页的文本内容，用于分析网页数据",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "要抓取的网页URL"
                    }
                },
                "required": ["url"]
            }
        ),
        Tool(
            name="get_page_data",
            description="获取网页特定数据",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "要获取数据的网页URL"
                    },
                    "selector": {
                        "type": "string",
                        "description": "CSS选择器，用于定位特定元素"
                    }
                },
                "required": ["url"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    if name == "fetch_content":
        return [TextContent(type="text", text=_fetch_web_content(arguments["url"]))]
    elif name == "get_page_data":
        selector = arguments.get("selector", "")
        return [TextContent(type="text", text=_get_page_data(arguments["url"], selector))]
    else:
        raise ValueError(f"Unknown tool: {name}")


def _fetch_web_content(url: str) -> str:
    try:
        session = _get_session()

        response = session.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "lxml")

        for script in soup(["script", "style"]):
            script.decompose()

        text = soup.get_text(separator="\n", strip=True)

        lines = [line for line in text.split("\n") if line.strip()]
        return "\n".join(lines[:500])

    except requests.RequestException as e:
        return f"Error fetching content: {str(e)}"


def _get_page_data(url: str, selector: str = "") -> str:
    try:
        session = _get_session()

        response = session.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "lxml")

        if selector:
            elements = soup.select(selector)
            if elements:
                return "\n".join([elem.get_text(strip=True) for elem in elements[:10]])
            return "Selector not found"

        return _fetch_web_content(url)

    except requests.RequestException as e:
        return f"Error fetching content: {str(e)}"


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
