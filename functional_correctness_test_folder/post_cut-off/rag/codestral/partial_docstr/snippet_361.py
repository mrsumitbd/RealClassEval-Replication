
from typing import Any
from pydantic import BaseModel
from langchain_core.tools import ToolCall


class OCIUtils:
    '''Utility functions for OCI Generative AI integration.'''

    @staticmethod
    def is_pydantic_class(obj: Any) -> bool:
        '''Check if an object is a Pydantic BaseModel subclass.'''
        return isinstance(obj, type) and issubclass(obj, BaseModel)

    @staticmethod
    def remove_signature_from_tool_description(name: str, description: str) -> str:
        '''
        Remove the tool signature and Args section from a tool description.
        The signature is typically prefixed to the description and followed
        by an Args section.
        '''
        # Remove the signature line (e.g., "tool_name(arg1: type, arg2: type)")
        lines = description.split('\n')
        if lines and lines[0].startswith(f"{name}("):
            lines = lines[1:]

        # Remove the Args section
        args_index = next((i for i, line in enumerate(lines)
                          if line.strip() == "Args:"), None)
        if args_index is not None:
            lines = lines[:args_index]

        return '\n'.join(lines).strip()

    @staticmethod
    def convert_oci_tool_call_to_langchain(tool_call: Any) -> ToolCall:
        '''Convert an OCI tool call to a LangChain ToolCall.'''
        return ToolCall(
            name=tool_call.tool_name,
            args=tool_call.tool_parameters,
            id=tool_call.tool_call_id
        )
