
from typing import Any
from pydantic import BaseModel
from langchain.schema.tool import ToolCall


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
        if not description:
            return description

        # Remove signature (e.g., "tool_name(arg1: type, arg2: type)")
        signature_prefix = f"{name}("
        if signature_prefix in description:
            description = description.split(signature_prefix, 1)[-1]
            description = description.split(")", 1)[-1].strip()

        # Remove Args section if present
        args_prefix = "Args:"
        if args_prefix in description:
            description = description.split(args_prefix)[0].strip()

        return description

    @staticmethod
    def convert_oci_tool_call_to_langchain(tool_call: Any) -> ToolCall:
        '''Convert an OCI tool call to a LangChain ToolCall.'''
        if not hasattr(tool_call, 'name') or not hasattr(tool_call, 'arguments'):
            raise ValueError(
                "Invalid OCI tool call: missing 'name' or 'arguments'")

        return ToolCall(
            name=tool_call.name,
            args=tool_call.arguments if isinstance(
                tool_call.arguments, dict) else {}
        )
