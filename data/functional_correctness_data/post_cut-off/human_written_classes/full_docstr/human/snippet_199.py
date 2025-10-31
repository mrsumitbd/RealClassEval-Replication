import textwrap
from typing import Optional
from viby.config import config
from viby.locale import get_text
from viby.viby_tool_search.commands import EmbedServerCommand
from viby.viby_tool_search.utils import get_mcp_tools_from_cache
from rich.panel import Panel
from rich.table import Table

class ToolsCommand:
    """
    工具管理命令类，提供工具嵌入向量更新和列出工具信息功能
    支持以下子命令：
    - embed - 嵌入向量管理，包含update、start、stop、status子命令
    - list - 列出所有可用的MCP工具
    - download - 检查并下载嵌入模型
    """

    def __init__(self):
        """初始化工具命令"""
        self.config = config
        self.embed_server_command = EmbedServerCommand()

    def list_tools(self) -> int:
        """列出所有可用的MCP工具"""
        try:
            console.print(Panel.fit(get_text('TOOLS', 'listing_tools'), title=get_text('TOOLS', 'tools_list_title')))
            try:
                server_tools_dict = get_mcp_tools_from_cache()
                if not server_tools_dict:
                    console.print(f"[bold yellow]{get_text('TOOLS', 'no_tools_found')}[/bold yellow]")
                    return 0
            except Exception as e:
                console.print(f"[bold red]{get_text('TOOLS', 'error_listing_tools')}: {str(e)}[/bold red]")
                logger.exception(get_text('TOOLS', 'tools_listing_failed'))
                return 1
            table = Table(title=get_text('TOOLS', 'available_tools_table_title'))
            table.add_column(get_text('TOOLS', 'tool_name_column'), style='cyan')
            table.add_column(get_text('TOOLS', 'description_column'))
            table.add_column(get_text('TOOLS', 'param_count_column'), justify='right')
            table.add_column(get_text('TOOLS', 'server_column'), style='dim')
            all_tools = []
            for server_name, tools in server_tools_dict.items():
                for tool in tools:
                    all_tools.append((tool.name, tool, server_name))
            for name, tool, server_name in sorted(all_tools, key=lambda x: x[0]):
                description = tool.description if hasattr(tool, 'description') else ''
                if callable(description):
                    try:
                        description = description()
                    except Exception:
                        description = get_text('TOOLS', 'description_unavailable')
                parameters = tool.inputSchema if hasattr(tool, 'inputSchema') else {}
                param_properties = parameters.get('properties', {}) if isinstance(parameters, dict) else {}
                param_count = len(param_properties)
                short_desc = textwrap.shorten(description, width=60, placeholder='...')
                table.add_row(name, short_desc, str(param_count), server_name)
            console.print(table)
            total_tools = sum((len(tools) for tools in server_tools_dict.values()))
            console.print(f"\n{get_text('TOOLS', 'total_tools')}: [bold cyan]{total_tools}[/bold cyan]")
            return 0
        except Exception as e:
            console.print(f"[bold red]{get_text('TOOLS', 'error_listing_tools')}: {str(e)}[/bold red]")
            logger.exception(get_text('TOOLS', 'tools_listing_failed'))
            return 1

    def run(self, embed_subcommand: Optional[str]=None) -> int:
        """
        管理嵌入向量服务，支持子命令：update、start、stop、status、download
        """
        if embed_subcommand is None:
            return self.embed_server_command.update_embeddings()
        return self.embed_server_command.run(embed_subcommand)