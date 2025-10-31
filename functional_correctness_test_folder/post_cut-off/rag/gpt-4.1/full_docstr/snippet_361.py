from typing import Any
import re

from langchain_core.tools import ToolCall


class OCIUtils:
    '''Utility functions for OCI Generative AI integration.'''

    @staticmethod
    def is_pydantic_class(obj: Any) -> bool:
        '''Check if an object is a Pydantic BaseModel subclass.'''
        try:
            from pydantic import BaseModel
            return isinstance(obj, type) and issubclass(obj, BaseModel)
        except ImportError:
            return False

    @staticmethod
    def remove_signature_from_tool_description(name: str, description: str) -> str:
        '''
        Remove the tool signature and Args section from a tool description.
        The signature is typically prefixed to the description and followed
        by an Args section.
        '''
        # Remove signature line (e.g., "tool_name(arg1: type, arg2: type) -> return_type")
        pattern = rf"^{re.escape(name)}\s*\(.*?\)\s*->.*?\n"
        desc = re.sub(pattern, '', description, flags=re.DOTALL | re.MULTILINE)
        # Remove Args section (from "Args:" to next section or end)
        desc = re.sub(r"(?s)Args:\s*.*?(?=\n\S|$)", '', desc)
        return desc.strip()

    @staticmethod
    def convert_oci_tool_call_to_langchain(tool_call: Any) -> ToolCall:
        '''Convert an OCI tool call to a LangChain ToolCall.'''
        # Assume tool_call is a dict-like object with keys: id, name, arguments
        return ToolCall(
            id=tool_call.get("id"),
            name=tool_call.get("name"),
            args=tool_call.get("arguments")
        )
