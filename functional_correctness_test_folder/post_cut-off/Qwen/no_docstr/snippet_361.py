
from typing import Any
from pydantic import BaseModel
from langchain.schema import ToolCall


class OCIUtils:

    @staticmethod
    def is_pydantic_class(obj: Any) -> bool:
        return isinstance(obj, type) and issubclass(obj, BaseModel)

    @staticmethod
    def remove_signature_from_tool_description(name: str, description: str) -> str:
        import re
        pattern = rf"{name}\(.*?\)"
        return re.sub(pattern, name, description)

    @staticmethod
    def convert_oci_tool_call_to_langchain(tool_call: Any) -> ToolCall:
        return ToolCall(
            name=tool_call.name,
            arguments=tool_call.arguments
        )
