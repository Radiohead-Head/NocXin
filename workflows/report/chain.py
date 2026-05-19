from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from config import MODEL_NAME, OPENAI_API_KEY, OPENAI_API_BASE_URL, REPORT_TEMPLATE


llm = ChatOpenAI(
    model=MODEL_NAME,
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_API_BASE_URL or None,
    temperature=0.7
)

prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一个专业的周报整理助手。你的任务是从网页内容中提取关键信息，并生成结构化的周报。

请从内容中提取并整理以下信息：
1. 本周工作概览
2. 关键数据和指标
3. 下周工作计划
4. 需要关注的问题

请用简洁专业的语言输出 Markdown 格式的周报。"""),
    ("human", "以下是网页内容：\n\n{content}\n\n请生成周报：")
])

report_chain = LLMChain(llm=llm, prompt=prompt)


def generate_weekly_report(web_content: str) -> str:
    """根据网页内容生成周报"""
    return report_chain.invoke({"content": web_content})["text"]