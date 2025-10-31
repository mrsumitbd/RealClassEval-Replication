from typing import Iterator, AsyncIterator, Dict, List, Any, Optional

class MockSettings:

    def __init__(self):
        self.pattern = ''
        self.response = DEFAULT_MOCK_RESPONSE
        self.available_tools = {}

    def set(self, pattern: str, response: str):
        """Set the pattern and response template"""
        self.pattern = pattern
        self.response = response

    def get(self) -> tuple[str, str]:
        """Get the current pattern and response template"""
        return (self.pattern, self.response)

    def add_tool(self, name: str, function):
        """Register a tool function"""
        self.available_tools[name] = function

    def clear_tools(self):
        """Clear registered tools"""
        self.available_tools = {}

    def get_tools(self) -> Dict[str, Any]:
        """Get available tools"""
        return self.available_tools