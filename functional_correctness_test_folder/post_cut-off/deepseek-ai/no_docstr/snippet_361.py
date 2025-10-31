
from typing import Any
from langchain_core.tools import ToolCall


class OCIUtils:

    @staticmethod
    def is_pydantic_class(obj: Any) -> bool:
        try:
            from pydantic import BaseModel
            return isinstance(obj, type) and issubclass(obj, BaseModel)
        except ImportError:
            return False

    @staticmethod
    def remove_signature_from_tool_description(name: str, description: str) -> str:
        if description.startswith(f"{name}("):
            return description.split(")")[-1].strip()
        return description

    @staticmethod
    def convert_oci_tool_call_to_langchain(tool_call: Any) -> ToolCall:
        return ToolCall(
            name=tool_call.name,
            args=tool_call.arguments,
            id=tool_call.id if hasattr(tool_call, "id") else None
        )
