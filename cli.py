import click
from config import REPORT_URL, OPENAI_API_KEY, MCP_SERVER_COMMAND, MCP_SERVER_URL
from tools.web_tools import fetch_web_content
from workflows.report.chain import generate_weekly_report
from workflows.report.mcp_chain import run_mcp_agent_task, generate_report_via_mcp


@click.group()
def cli():
    """智能助手 CLI - 基于 LangChain + MCP"""
    pass


@cli.command()
@click.option("--output", "-o", default=None, help="输出文件路径")
def report(output):
    """生成周报（自动选择最佳数据源）"""
    url = REPORT_URL
    click.echo(f"正在从 {url} 获取内容...")

    if MCP_SERVER_COMMAND or MCP_SERVER_URL:
        click.echo("使用 MCP 协议获取数据...")
        report = generate_report_via_mcp(url)
    else:
        click.echo("使用 HTTP 直接获取数据...")
        content = fetch_web_content.invoke(url)
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
def version():
    """显示版本信息"""
    click.echo("Weekly Report CLI v1.0.0 (LangChain + MCP)")


if __name__ == "__main__":
    cli()