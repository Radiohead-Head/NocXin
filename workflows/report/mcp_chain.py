from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from config import MODEL_NAME, OPENAI_API_KEY, OPENAI_API_BASE_URL
from tools.mcp_tools import mcp_fetch_web_content, mcp_get_page_data
from workflows.report.chain import generate_weekly_report


llm = ChatOpenAI(
    model=MODEL_NAME,
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_API_BASE_URL or None,
    temperature=0
)

prompt = PromptTemplate.from_template("""你是一个智能助手，负责通过 MCP 协议获取网页数据并生成周报。

可用工具（MCP 协议）：
- mcp_fetch_web_content: 通过 MCP 获取指定URL的网页内容
- mcp_get_page_data: 通过 MCP 获取网页特定数据

工作流程：
1. 使用 mcp_fetch_web_content 或 mcp_get_page_data 获取网页数据
2. 分析数据内容
3. 生成周报

输入: {input}
{agent_scratchpad}
""")


tools = [mcp_fetch_web_content, mcp_get_page_data]
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


def run_mcp_agent_task(task: str) -> str:
    """运行 MCP Agent 处理任务"""
    result = agent_executor.invoke({"input": task})
    return result["output"]


def generate_report_via_mcp(url: str) -> str:
    """通过 MCP 获取数据并生成周报"""
    content = mcp_fetch_web_content.invoke({"url": url})
    if content.startswith("Error"):
        return content
    return generate_weekly_report(content)