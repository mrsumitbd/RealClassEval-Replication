
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
        lines = description.split('\n')
        # Find the index of the first line that doesn't start with a space or a '('
        # and is not empty
        for i, line in enumerate(lines):
            stripped_line = line.strip()
            if stripped_line and not stripped_line.startswith('(') and not line.startswith(' '):
                # Check if 'Args:' is present in the remaining lines
                if 'Args:' in '\n'.join(lines[i+1:]):
                    # Return the description without the signature and Args section
                    return '\n'.join([l for l in lines[i+1:] if not l.strip().startswith('Args:') and not l.strip().startswith('- ')])
                else:
                    # If 'Args:' is not found, return the description from the current line onwards
                    return '\n'.join(lines[i:])
        # If no such line is found, return an empty string
        return ''

    @staticmethod
    def convert_oci_tool_call_to_langchain(tool_call: Any) -> ToolCall:
        '''Convert an OCI tool call to a LangChain ToolCall.'''
        return ToolCall(
            name=tool_call.name,
            args=tool_call.arguments,
            id=tool_call.id
        )
