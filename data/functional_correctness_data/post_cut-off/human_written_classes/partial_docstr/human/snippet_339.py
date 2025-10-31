from typing import Any
from datetime import datetime
from mcp.types import GetPromptResult, Prompt, PromptArgument, PromptMessage, TextContent

class PromptTemplate:
    """Prompt template"""

    def __init__(self, name: str, description: str, template: str, arguments: list[PromptArgument]=None, category: str='general'):
        self.name = name
        self.description = description
        self.template = template
        self.arguments = arguments or []
        self.category = category
        self.created_at = datetime.now()

    def render(self, arguments: dict[str, Any]) -> str:
        """Render template content"""
        content = self.template
        for key, value in arguments.items():
            placeholder = f'{{{key}}}'
            content = content.replace(placeholder, str(value))
        return content