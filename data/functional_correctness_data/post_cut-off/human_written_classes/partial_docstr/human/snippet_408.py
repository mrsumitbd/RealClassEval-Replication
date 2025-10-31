from collections.abc import Callable, Iterator
from fraim.util.files.basepath import BasePathFS
from fraim.core.tools import BaseTool, ToolError

class FilesystemTools:
    """
    Direct interface to filesystem utilities for project exploration and file operations.

    This class provides fraim-compatible tools that use the filesystem utilities to:
    - Search text patterns across files with ripgrep
    - List directory contents recursively
    - Read file contents with optional line ranges

    The tools automatically use BasePathFS for path sandboxing and provide a clean
    interface for AI agents to explore file systems safely.
    """

    def __init__(self, project_path: str):
        self.project_path = project_path
        self.fs = BasePathFS(project_path)
        self.tools: list[BaseTool] = [GrepTool.create(self.fs), ListDirTool.create(self.fs), ReadFileTool.create(self.fs)]

    def __iter__(self) -> Iterator[BaseTool]:
        return iter(self.tools)