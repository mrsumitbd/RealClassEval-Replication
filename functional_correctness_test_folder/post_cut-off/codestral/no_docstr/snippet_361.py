
from typing import Any
from pydantic import BaseModel
from langchain_core.tools import ToolCall


class OCIUtils:

    @staticmethod
    def is_pydantic_class(obj: Any) -> bool:
        return isinstance(obj, type) and issubclass(obj, BaseModel)

    @staticmethod
    def remove_signature_from_tool_description(name: str, description: str) -> str:
        signature = f"{name}("
        if description.startswith(signature):
            description = description[len(signature):]
            if description.endswith(")"):
                description = description[:-1]
        return description.strip()

    @staticmethod
    def convert_oci_tool_call_to_langchain(tool_call: Any) -> ToolCall:
        return ToolCall(name=tool_call.name, args=tool_call.arguments, id=tool_call.id)
