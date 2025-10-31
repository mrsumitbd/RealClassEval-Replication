
from typing import Any
from pydantic import BaseModel
from langchain_core.tools import ToolCall


class OCIUtils:

    @staticmethod
    def is_pydantic_class(obj: Any) -> bool:
        '''Check if an object is a Pydantic BaseModel subclass.'''
        return isinstance(obj, type) and issubclass(obj, BaseModel)

    @staticmethod
    def remove_signature_from_tool_description(name: str, description: str) -> str:
        lines = description.split('\n')
        signature_line = f'{name}('
        for i, line in enumerate(lines):
            if line.strip().startswith(signature_line):
                return '\n'.join(lines[i+1:])
        return description

    @staticmethod
    def convert_oci_tool_call_to_langchain(tool_call: Any) -> ToolCall:
        '''Convert an OCI tool call to a LangChain ToolCall.'''
        return ToolCall(
            name=tool_call.name,
            args=tool_call.arguments,
            id=tool_call.id
        )
