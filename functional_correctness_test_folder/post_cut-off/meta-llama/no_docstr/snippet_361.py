
from typing import Any
from pydantic import BaseModel
from langchain.schema import ToolCall


class OCIUtils:

    @staticmethod
    def is_pydantic_class(obj: Any) -> bool:
        return isinstance(obj, type) and issubclass(obj, BaseModel)

    @staticmethod
    def remove_signature_from_tool_description(name: str, description: str) -> str:
        lines = description.split('\n')
        signature_lines = []
        for line in lines:
            if line.strip().startswith(name) and '(' in line and ')' in line:
                signature_lines.append(line)
        for signature_line in signature_lines:
            lines.remove(signature_line)
        return '\n'.join(lines).strip()

    @staticmethod
    def convert_oci_tool_call_to_langchain(tool_call: Any) -> ToolCall:
        if not hasattr(tool_call, 'tool_name') or not hasattr(tool_call, 'parameters'):
            raise ValueError("Invalid tool call object")

        return ToolCall(
            name=tool_call.tool_name,
            args=tool_call.parameters,
            id=getattr(tool_call, 'id', None)
        )
