from typing import Optional
from langchain_core.tools import tool
import requests
from bs4 import BeautifulSoup


@tool
def fetch_web_content(url: str) -> str:
    """获取指定网页的文本内容，用于分析网页数据。

    Args:
        url: 要抓取的网页URL

    Returns:
        网页的文本内容，如果失败则返回错误信息
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "lxml")

        for script in soup(["script", "style"]):
            script.decompose()

        text = soup.get_text(separator="\n", strip=True)

        lines = [line for line in text.split("\n") if line.strip()]
        return "\n".join(lines[:500])

    except requests.RequestException as e:
        return f"Error fetching content: {str(e)}"


@tool
def parse_weekly_data(content: str) -> dict:
    """解析周报数据内容，提取关键信息。

    Args:
        content: 网页文本内容

    Returns:
        包含解析后关键数据的字典
    """
    return {
        "status": "ready",
        "content_preview": content[:200] if len(content) > 200 else content
    }