
from typing import Any
from pydantic import BaseModel
import re
from langchain.schema import ToolCall


class OCIUtils:
    '''Utility functions for OCI Generative AI integration.'''
    @staticmethod
    def is_pydantic_class(obj: Any) -> bool:
        '''Check if an object is a Pydantic BaseModel subclass.'''
        return isinstance(obj, type) and issubclass(obj, BaseModel) and obj != BaseModel

    @staticmethod
    def remove_signature_from_tool_description(name: str, description: str) -> str:
        '''
        Remove the tool signature and Args section from a tool description.
        The signature is typically prefixed to the description and followed
        by an Args section.
        '''
        # Remove the function signature
        signature_pattern = rf'^{re.escape(name)}\(.*?\)\s*:\s*.*?\n'
        description = re.sub(signature_pattern, '',
                             description, flags=re.DOTALL)

        # Remove the Args section
        args_section_pattern = r'^Args:\s*.*?(?=\n[A-Z][a-z]+:|\Z)', re.MULTILINE | re.DOTALL
        description = re.sub(args_section_pattern, '', description)

        return description.strip()

    @staticmethod
    def convert_oci_tool_call_to_langchain(tool_call: Any) -> ToolCall:
        '''Convert an OCI tool call to a LangChain ToolCall.'''
        # Assuming tool_call has attributes 'name' and 'arguments'
        return ToolCall(
            name=tool_call.name,
            arguments=tool_call.arguments
        )
