
from typing import Any
import re

try:
    from pydantic import BaseModel
except ImportError:
    BaseModel = None

try:
    from langchain_core.tools import ToolCall
except ImportError:
    # Minimal ToolCall stub for compatibility
    class ToolCall:
        def __init__(self, id, name, args):
            self.id = id
            self.name = name
            self.args = args


class OCIUtils:

    @staticmethod
    def is_pydantic_class(obj: Any) -> bool:
        '''Check if an object is a Pydantic BaseModel subclass.'''
        if BaseModel is None:
            return False
        try:
            return isinstance(obj, type) and issubclass(obj, BaseModel)
        except Exception:
            return False

    @staticmethod
    def remove_signature_from_tool_description(name: str, description: str) -> str:
        # Remove lines starting with the function signature (e.g., "name(")
        pattern = rf"^{re.escape(name)}\s*\(.*\)\s*"
        lines = description.splitlines()
        new_lines = []
        for line in lines:
            if not re.match(pattern, line.strip()):
                new_lines.append(line)
        return "\n".join(new_lines).strip()

    @staticmethod
    def convert_oci_tool_call_to_langchain(tool_call: Any) -> ToolCall:
        '''Convert an OCI tool call to a LangChain ToolCall.'''
        # Expecting tool_call to be a dict with keys: id, function (with name and arguments)
        if hasattr(tool_call, "id"):
            call_id = getattr(tool_call, "id")
        else:
            call_id = tool_call.get("id")
        if hasattr(tool_call, "function"):
            function = getattr(tool_call, "function")
        else:
            function = tool_call.get("function")
        if hasattr(function, "name"):
            name = getattr(function, "name")
        else:
            name = function.get("name")
        if hasattr(function, "arguments"):
            args = getattr(function, "arguments")
        else:
            args = function.get("arguments")
        return ToolCall(id=call_id, name=name, args=args)
