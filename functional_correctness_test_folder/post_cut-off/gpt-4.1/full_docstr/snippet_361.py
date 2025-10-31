
from typing import Any
import re

try:
    from pydantic import BaseModel
except ImportError:
    BaseModel = None

try:
    from langchain_core.tools import ToolCall
except ImportError:
    # Dummy ToolCall for type hinting if langchain_core is not installed
    class ToolCall:
        def __init__(self, id, name, args):
            self.id = id
            self.name = name
            self.args = args


class OCIUtils:
    '''Utility functions for OCI Generative AI integration.'''

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
        '''
        Remove the tool signature and Args section from a tool description.
        The signature is typically prefixed to the description and followed
        by an Args section.
        '''
        # Remove signature line (e.g., "tool_name(arg1: type, arg2: type) -> return_type")
        # and the Args section if present.
        # The signature is usually the first line, followed by a blank line or Args.
        # The Args section starts with "Args:" and may have indented lines after.
        # We'll remove from the start up to the first non-signature, non-Args content.

        # Remove the signature line if it matches the pattern
        lines = description.splitlines()
        new_lines = []
        in_args_section = False
        args_section_started = False

        # Regex to match a function signature at the start
        signature_regex = re.compile(
            rf"^{re.escape(name)}\s*\(.*\)\s*(->.*)?\s*$")

        i = 0
        # Remove signature line(s)
        while i < len(lines):
            if signature_regex.match(lines[i].strip()):
                i += 1
                # Skip possible blank line after signature
                while i < len(lines) and lines[i].strip() == "":
                    i += 1
                break
            else:
                break

        # Remove Args section if present
        while i < len(lines):
            if lines[i].strip().lower() == "args:":
                args_section_started = True
                i += 1
                # Skip indented lines (arguments descriptions)
                while i < len(lines):
                    if lines[i].strip() == "":
                        i += 1
                        continue
                    if re.match(r"^\s", lines[i]):
                        i += 1
                    else:
                        break
                # Skip possible blank line after Args section
                while i < len(lines) and lines[i].strip() == "":
                    i += 1
                break
            else:
                break

        # The rest is the cleaned description
        cleaned = "\n".join(lines[i:]).lstrip("\n")
        return cleaned

    @staticmethod
    def convert_oci_tool_call_to_langchain(tool_call: Any) -> ToolCall:
        '''Convert an OCI tool call to a LangChain ToolCall.'''
        # Assume tool_call is a dict or object with 'id', 'name', and 'arguments'
        # LangChain ToolCall expects id, name, args (args is a dict)
        if isinstance(tool_call, dict):
            id_ = tool_call.get("id")
            name = tool_call.get("name")
            args = tool_call.get("arguments") or tool_call.get("args") or {}
        else:
            id_ = getattr(tool_call, "id", None)
            name = getattr(tool_call, "name", None)
            args = getattr(tool_call, "arguments", None)
            if args is None:
                args = getattr(tool_call, "args", {})
            if args is None:
                args = {}

        # If arguments is a JSON string, parse it
        if isinstance(args, str):
            import json
            try:
                args = json.loads(args)
            except Exception:
                args = {}

        return ToolCall(id=id_, name=name, args=args)
