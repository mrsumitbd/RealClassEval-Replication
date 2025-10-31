
from typing import Any
from pydantic import BaseModel
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
        import re
        # Define a regex pattern to match the function signature and Args section
        pattern = rf'^{re.escape(name)}\(.*?\)\s*Args:\s*.*?(?=\n\n|\Z)', re.DOTALL | re.MULTILINE
        # Substitute the matched pattern with an empty string
        cleaned_description = re.sub(pattern, '', description).strip()
        return cleaned_description

    @staticmethod
    def convert_oci_tool_call_to_langchain(tool_call: Any) -> ToolCall:
        '''Convert an OCI tool call to a LangChain ToolCall.'''
        # Assuming tool_call has attributes 'name' and 'arguments'
        return ToolCall(
            name=tool_call.name,
            arguments=tool_call.arguments
        )
