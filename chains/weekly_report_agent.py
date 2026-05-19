from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from config import MODEL_NAME, OPENAI_API_KEY, OPENAI_API_BASE_URL
from tools.web_tools import fetch_web_content, parse_weekly_data


llm = ChatOpenAI(
    model=MODEL_NAME,
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_API_BASE_URL or None,
    temperature=0
)

prompt = PromptTemplate.from_template("""你是一个智能助手，负责从网页获取数据并生成周报。

可用工具：
- fetch_web_content: 获取指定URL的网页内容
- parse_weekly_data: 解析周报数据

工作流程：
1. 使用 fetch_web_content 获取网页内容
2. 使用 parse_weekly_data 解析数据
3. 根据解析结果生成最终周报

输入: {input}
{agent_scratchpad}
""")


tools = [fetch_web_content, parse_weekly_data]
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


def run_agent_task(task: str) -> str:
    """运行 Agent 处理任务"""
    result = agent_executor.invoke({"input": task})
    return result["output"]