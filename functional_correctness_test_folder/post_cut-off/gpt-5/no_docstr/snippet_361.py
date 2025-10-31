from __future__ import annotations

import json
from typing import Any, Dict, Optional

try:
    from langchain_core.messages import ToolCall  # type: ignore
except Exception:
    try:
        from langchain.schema.messages import ToolCall  # type: ignore
    except Exception:
        from dataclasses import dataclass

        @dataclass
        class ToolCall:  # type: ignore
            name: str
            args: Dict[str, Any]
            id: Optional[str] = None


class OCIUtils:

    @staticmethod
    def is_pydantic_class(obj: Any) -> bool:
        try:
            from pydantic import BaseModel  # type: ignore
        except Exception:
            return False
        return isinstance(obj, type) and issubclass(obj, BaseModel)

    @staticmethod
    def remove_signature_from_tool_description(name: str, description: str) -> str:
        if not isinstance(description, str) or not description:
            return description

        text = description.lstrip()

        prefixes = [f"{name}(", f"def {name}("]
        matched = None
        for p in prefixes:
            if text.startswith(p):
                matched = p
                break
        if matched is None:
            return description

        end_idx = text.find(")")
        if end_idx == -1:
            return description

        rest = text[end_idx + 1:].lstrip()

        for sep in (":", "-", "—", "->"):
            if rest.startswith(sep):
                rest = rest[len(sep):].lstrip()
                break

        if not rest:
            # If no text remains on the first line, drop it and keep subsequent lines
            lines = description.splitlines()
            if len(lines) <= 1:
                return ""
            return "\n".join(lines[1:]).lstrip()

        # Preserve any original leading whitespace before the signature
        leading_ws_len = len(description) - len(description.lstrip())
        leading_ws = description[:leading_ws_len]
        # Append the remaining original lines after the first line
        original_lines = description.splitlines()
        if len(original_lines) > 1:
            tail = "\n".join(original_lines[1:])
            if tail:
                rest = rest + "\n" + tail
        return leading_ws + rest

    @staticmethod
    def convert_oci_tool_call_to_langchain(tool_call: Any) -> ToolCall:
        def _get(d: Any, *keys: str) -> Any:
            for k in keys:
                if isinstance(d, dict) and k in d:
                    return d[k]
                if hasattr(d, k):
                    return getattr(d, k)
            return None

        name = None
        args: Any = None
        call_id = None

        # Common OpenAI-style: {"id": "...", "type": "function", "function": {"name": "...", "arguments": "..."}}
        function = _get(tool_call, "function")
        if function:
            name = _get(function, "name")
            args = _get(function, "arguments")
            call_id = _get(tool_call, "id")

        # Direct fields: {"name": "...", "arguments": ...}
        if name is None:
            name = _get(tool_call, "name", "toolName", "tool_name")
        if args is None:
            args = _get(tool_call, "arguments", "args",
                        "parameters", "toolParameters", "tool_params")
        if call_id is None:
            call_id = _get(tool_call, "id", "call_id", "callId")

        # Parse arguments if needed
        if args is None:
            parsed_args: Dict[str, Any] = {}
        elif isinstance(args, str):
            try:
                loaded = json.loads(args)
                parsed_args = loaded if isinstance(loaded, dict) else {
                    "value": loaded}
            except Exception:
                parsed_args = {"value": args}
        elif isinstance(args, dict):
            parsed_args = args
        else:
            # Try to coerce to dict
            try:
                parsed_args = dict(args)  # type: ignore
            except Exception:
                parsed_args = {"value": args}

        if not name:
            # Fallback generic name
            name = "unknown_tool"

        return ToolCall(name=name, args=parsed_args, id=call_id)
