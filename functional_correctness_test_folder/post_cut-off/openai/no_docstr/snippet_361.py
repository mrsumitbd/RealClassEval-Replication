
from __future__ import annotations

from typing import Any, Dict, Optional
import json

try:
    from pydantic import BaseModel
except Exception:
    BaseModel = None  # type: ignore

try:
    from langchain.schema import ToolCall
except Exception:
    # Minimal fallback definition if langchain is not installed
    class ToolCall:
        def __init__(self, name: str, args: Dict[str, Any], id: Optional[str] = None):
            self.name = name
            self.args = args
            self.id = id

        def __repr__(self):
            return f"ToolCall(name={self.name!r}, args={self.args!r}, id={self.id!r})"


class OCIUtils:
    @staticmethod
    def is_pydantic_class(obj: Any) -> bool:
        """
        Return True if `obj` is a Pydantic BaseModel instance or subclass.
        """
        if BaseModel is None:
            return False
        if isinstance(obj, BaseModel):
            return True
        if isinstance(obj, type) and issubclass(obj, BaseModel):
            return True
        return False

    @staticmethod
    def remove_signature_from_tool_description(name: str, description: str) -> str:
        """
        Remove any signature block from a tool description.
        A signature block is assumed to start with either "##" or "Signature:".
        """
        markers = ["##", "Signature:"]
        idx = len(description)
        for marker in markers:
            pos = description.find(marker)
            if pos != -1 and pos < idx:
                idx = pos
        cleaned = description[:idx].rstrip()
        return cleaned

    @staticmethod
    def convert_oci_tool_call_to_langchain(tool_call: Any) -> ToolCall:
        """
        Convert an OCI tool call (dict or object) into a LangChain ToolCall.
        Expected fields:
            - name (str)
            - arguments (JSON string or dict)
            - id (optional str)
        """
        # Extract name
        name = getattr(tool_call, "name", None)
        if name is None and isinstance(tool_call, dict):
            name = tool_call.get("name")
        if name is None:
            raise ValueError("tool_call must have a 'name' field")

        # Extract arguments
        args_raw = getattr(tool_call, "arguments", None)
        if args_raw is None and isinstance(tool_call, dict):
            args_raw = tool_call.get("arguments")
        if args_raw is None:
            args = {}
        elif isinstance(args_raw, str):
            try:
                args = json.loads(args_raw)
            except json.JSONDecodeError:
                args = {}
        elif isinstance(args_raw, dict):
            args = args_raw
        else:
            args = {}

        # Extract id
        tool_id = getattr(tool_call, "id", None)
        if tool_id is None and isinstance(tool_call, dict):
            tool_id = tool_call.get("id")

        return ToolCall(name=name, args=args, id=tool_id)
