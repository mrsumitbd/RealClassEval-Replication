from fraim.core.tools import BaseTool, ToolError
from mcp_server_tree_sitter.api import get_language_registry, get_project_registry, get_tree_cache, register_project
from mcp_server_tree_sitter.exceptions import FileAccessError, ProjectError, QueryError
from collections.abc import Callable, Iterator

class TreeSitterTools:
    """
    Direct interface to tree-sitter code analysis tools for project exploration and parsing.

    This class provides fraim-compatible tools that use the tree-sitter library to:
    - List and filter project files
    - Read file contents with optional line ranges
    - Generate Abstract Syntax Trees (ASTs) for code analysis

    Why direct integration instead of MCP server?
    - Custom tool descriptions and parameter handling for LLM agents
    - Automatic project registration eliminates manual setup steps
    - No external server process or binary dependencies required
    - Simplified deployment and configuration

    The tools automatically register the project with tree-sitter on initialization
    and provide a clean interface for AI agents to explore codebases.
    """

    def __init__(self, project_path: str, project_name: str | None=None):
        self.project_path = project_path
        self.project_name = project_name or project_path.split('/')[-1]
        try:
            self.project = get_project_registry().get_project(self.project_name)
        except ProjectError:
            register_project(path=self.project_path, name=self.project_name)
            self.project = get_project_registry().get_project(self.project_name)
        self.tools: list[TreeSitterBaseTool] = [ListFilesTool.create(self.project), GetFileContentTool.create(self.project), GetFileAstTool.create(self.project), GetAstNodeAtPositionTool.create(self.project), FindSymbolUsageTool.create(self.project), FindFunctionDefinitionTool.create(self.project), QueryCodeTool.create(self.project), SearchTextTool.create(self.project)]

    def __iter__(self) -> Iterator[BaseTool]:
        return iter(self.tools)