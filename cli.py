import click
from config import WEB_PAGE_URL, OPENAI_API_KEY, MCP_SERVER_COMMAND, MCP_SERVER_URL
from tools.web_tools import fetch_web_content
from chains.weekly_report import generate_weekly_report
from chains.weekly_report_agent import run_agent_task
from chains.mcp_report_agent import run_mcp_agent_task, generate_report_via_mcp


@click.group()
def cli():
    """周报生成命令行工具 - 基于 LangChain + MCP"""
    pass


@cli.command()
@click.option("--url", "-u", default=WEB_PAGE_URL, help="网页URL")
@click.option("--output", "-o", default=None, help="输出文件路径")
def simple(url, output):
    """使用简单 Chain 模式生成周报"""
    click.echo(f"正在从 {url} 获取内容...")

    content = fetch_web_content.invoke(url)
    click.echo("内容获取成功，正在生成周报...")

    report = generate_weekly_report(content)

    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(report)
        click.echo(f"周报已保存到: {output}")
    else:
        click.echo("\n" + "=" * 50)
        click.echo("生成的周报:")
        click.echo("=" * 50)
        click.echo(report)


@cli.command()
@click.option("--url", "-u", default=WEB_PAGE_URL, help="网页URL")
@click.option("--output", "-o", default=None, help="输出文件路径")
def agent(url, output):
    """使用 Agent 模式生成周报（支持复杂推理）"""
    click.echo(f"正在使用 Agent 模式处理 {url}...")

    task = f"请从 {url} 获取网页内容，解析数据后生成周报"
    report = run_agent_task(task)

    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(report)
        click.echo(f"周报已保存到: {output}")
    else:
        click.echo("\n" + "=" * 50)
        click.echo("生成的周报:")
        click.echo("=" * 50)
        click.echo(report)


@cli.command()
@click.option("--url", "-u", default=WEB_PAGE_URL, help="网页URL")
@click.option("--output", "-o", default=None, help="输出文件路径")
def mcp(url, output):
    """使用 MCP 协议获取网页数据并生成周报"""
    if not MCP_SERVER_COMMAND and not MCP_SERVER_URL:
        click.echo("错误: 请设置 MCP_SERVER_COMMAND 或 MCP_SERVER_URL 环境变量")
        return

    click.echo(f"正在通过 MCP 从 {url} 获取内容...")

    report = generate_report_via_mcp(url)

    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(report)
        click.echo(f"周报已保存到: {output}")
    else:
        click.echo("\n" + "=" * 50)
        click.echo("生成的周报:")
        click.echo("=" * 50)
        click.echo(report)


@cli.command()
def version():
    """显示版本信息"""
    click.echo("Weekly Report CLI v1.0.0 (LangChain + MCP)")


if __name__ == "__main__":
    cli()