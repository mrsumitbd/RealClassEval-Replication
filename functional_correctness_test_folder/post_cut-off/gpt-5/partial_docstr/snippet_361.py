from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional

try:
    from langchain_core.messages import ToolCall  # type: ignore
except Exception:
    @dataclass
    class ToolCall:  # fallback if langchain_core is unavailable
        name: str
        args: Dict[str, Any]
        id: Optional[str] = None


class OCIUtils:

    @staticmethod
    def is_pydantic_class(obj: Any) -> bool:
        '''Check if an object is a Pydantic BaseModel subclass.'''
        if not isinstance(obj, type):
            return False
        bases = []
        try:
            from pydantic import BaseModel as PydanticBaseModel  # type: ignore
            bases.append(PydanticBaseModel)
        except Exception:
            pass
        try:
            from pydantic.v1 import BaseModel as PydanticV1BaseModel  # type: ignore
            bases.append(PydanticV1BaseModel)
        except Exception:
            pass
        if not bases:
            return False
        return issubclass(obj, tuple(bases))

    @staticmethod
    def remove_signature_from_tool_description(name: str, description: str) -> str:
        if not description:
            return description
        text = description.strip()

        # Pattern 1: name(args) - description OR name(args): description
        pattern = re.compile(
            rf'^\s*{re.escape(name)}\s*\([^)]*\)\s*[:\-–—]\s*', re.IGNORECASE)
        new_text = pattern.sub('', text, count=1)
        if new_text != text:
            return new_text.strip()

        # Pattern 2: name(args) description (no explicit separator)
        if text.lower().startswith(name.lower() + '('):
            close_idx = text.find(')')
            if close_idx != -1 and close_idx + 1 < len(text):
                remainder = text[close_idx + 1:].lstrip(" -–—:").strip()
                if remainder:
                    return remainder

        return text

    @staticmethod
    def convert_oci_tool_call_to_langchain(tool_call: Any) -> ToolCall:
        '''Convert an OCI tool call to a LangChain ToolCall.'''
        if tool_call is None:
            raise ValueError("tool_call cannot be None")

        def getter(obj: Any, key: str) -> Any:
            if isinstance(obj, Mapping):
                return obj.get(key)
            return getattr(obj, key, None)

        call_id = getter(tool_call, "id") or getter(tool_call, "call_id")
        function_block = getter(tool_call, "function") or getter(
            tool_call, "tool") or tool_call

        name = getter(function_block, "name")
        args_raw = getter(function_block, "arguments") or getter(
            function_block, "args") or getter(function_block, "parameters")

        # Parse arguments
        args: Dict[str, Any]
        if isinstance(args_raw, str):
            try:
                parsed = json.loads(args_raw)
                args = parsed if isinstance(parsed, dict) else {
                    "value": parsed}
            except Exception:
                args = {"value": args_raw}
        elif isinstance(args_raw, Mapping):
            args = dict(args_raw)
        elif args_raw is None:
            args = {}
        else:
            args = {"value": args_raw}

        if not name or not isinstance(name, str):
            raise ValueError("Invalid tool_call: missing function name")

        return ToolCall(name=name, args=args, id=call_id)
