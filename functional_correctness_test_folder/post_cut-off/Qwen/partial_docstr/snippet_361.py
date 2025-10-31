
from typing import Any
from pydantic import BaseModel
from langchain.schema import ToolCall


class OCIUtils:

    @staticmethod
    def is_pydantic_class(obj: Any) -> bool:
        '''Check if an object is a Pydantic BaseModel subclass.'''
        return isinstance(obj, type) and issubclass(obj, BaseModel) and obj != BaseModel

    @staticmethod
    def remove_signature_from_tool_description(name: str, description: str) -> str:
        '''Remove the function signature from the tool description.'''
        import re
        pattern = rf'{name}\(.*?\)\s*->\s*.*?\n'
        return re.sub(pattern, '', description, flags=re.DOTALL)

    @staticmethod
    def convert_oci_tool_call_to_langchain(tool_call: Any) -> ToolCall:
        '''Convert an OCI tool call to a LangChain ToolCall.'''
        return ToolCall(
            name=tool_call.name,
            arguments=tool_call.arguments
        )
