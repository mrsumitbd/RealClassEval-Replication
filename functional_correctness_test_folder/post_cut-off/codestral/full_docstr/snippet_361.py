
from typing import Any
from pydantic import BaseModel
from langchain.schema import ToolCall


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
        # Find the start of the signature
        signature_start = description.find(name)
        if signature_start == -1:
            return description

        # Find the end of the signature
        signature_end = description.find('Args:', signature_start)
        if signature_end == -1:
            return description[:signature_start].strip()

        # Remove the signature and Args section
        return description[:signature_start].strip() + description[signature_end + len('Args:'):].strip()

    @staticmethod
    def convert_oci_tool_call_to_langchain(tool_call: Any) -> ToolCall:
        '''Convert an OCI tool call to a LangChain ToolCall.'''
        return ToolCall(
            name=tool_call.name,
            args=tool_call.args,
            id=tool_call.id,
            type=tool_call.type
        )
