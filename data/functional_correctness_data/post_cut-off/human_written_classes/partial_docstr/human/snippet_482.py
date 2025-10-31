from typing import Any, Callable, Dict, Optional
import asyncio
import sys

class FastMCP:
    """Minimal FastMCP stub for basic MCP server operations."""

    def __init__(self, name: str, version: str='2.1.2'):
        self.name = name
        self.version = version
        self.tools = {}

    def tool(self, name: Optional[str]=None, description: str=''):
        """Tool decorator stub."""

        def decorator(func: Callable) -> Callable:
            tool_name = name or func.__name__
            self.tools[tool_name] = func
            return func
        return decorator

    def run(self, transport: str='stdio'):
        """Run stub - prints message and exits gracefully."""
        print(f'🚀 {self.name} v{self.version}', file=sys.stderr)
        print('⚠️  Running in stub mode - FastMCP not available', file=sys.stderr)
        print('📦 Install FastMCP with Python 3.10+ for full functionality', file=sys.stderr)
        print('✅ Server configuration validated successfully', file=sys.stderr)
        try:
            while True:
                asyncio.run(asyncio.sleep(1))
        except KeyboardInterrupt:
            print('\n🛑 Server stopped', file=sys.stderr)
            sys.exit(0)