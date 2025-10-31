
from typing import Any
import re


class ToolCall:
    def __init__(self, name: str, arguments: dict):
        self.name = name
        self.arguments = arguments


class OCIUtils:

    @staticmethod
    def is_pydantic_class(obj: Any) -> bool:
        try:
            from pydantic import BaseModel
        except ImportError:
            return False
        if isinstance(obj, type):
            return issubclass(obj, BaseModel)
        return isinstance(obj, BaseModel)

    @staticmethod
    def remove_signature_from_tool_description(name: str, description: str) -> str:
        # Remove the function signature from the start of the description if present
        # e.g. "foo(bar: int, baz: str) - This is a function." -> "This is a function."
        pattern = rf"^{re.escape(name)}\s*\([^\)]*\)\s*-?\s*"
        return re.sub(pattern, "", description, count=1).strip()

    @staticmethod
    def convert_oci_tool_call_to_langchain(tool_call: Any) -> ToolCall:
        # Assume tool_call is a dict with 'name' and 'arguments' keys
        if hasattr(tool_call, 'name') and hasattr(tool_call, 'arguments'):
            name = getattr(tool_call, 'name')
            arguments = getattr(tool_call, 'arguments')
        elif isinstance(tool_call, dict):
            name = tool_call.get('name')
            arguments = tool_call.get('arguments')
        else:
            raise ValueError(
                "tool_call must be a dict or have 'name' and 'arguments' attributes")
        if isinstance(arguments, str):
            import json
            try:
                arguments = json.loads(arguments)
            except Exception:
                arguments = {}
        return ToolCall(name, arguments)
