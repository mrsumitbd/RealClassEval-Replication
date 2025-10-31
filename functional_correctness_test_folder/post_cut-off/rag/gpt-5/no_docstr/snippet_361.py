from typing import Any
import json
import re

try:
    from langchain_core.messages import ToolCall
except Exception:  # pragma: no cover
    ToolCall = Any  # Fallback for environments without langchain_core


class OCIUtils:
    """Utility functions for OCI Generative AI integration."""

    @staticmethod
    def is_pydantic_class(obj: Any) -> bool:
        """Check if an object is a Pydantic BaseModel subclass."""
        if not isinstance(obj, type):
            return False
        try:
            from pydantic import BaseModel  # type: ignore
        except Exception:
            return False
        try:
            return issubclass(obj, BaseModel)
        except Exception:
            return False

    @staticmethod
    def remove_signature_from_tool_description(name: str, description: str) -> str:
        """
        Remove the tool signature and Args section from a tool description.
        The signature is typically prefixed to the description and followed
        by an Args section.
        """
        if not description:
            return ""

        desc = description.strip()

        # Remove leading signature line like: name(a: int, b: str) -> bool:
        sig_pattern = rf"^\s*{re.escape(name)}\s*\([^)]*\)\s*(?:->\s*[^\n:]+)?\s*:?\s*-?\s*"
        desc = re.sub(sig_pattern, "", desc, count=1)

        # Remove an "Args:" section and its indented content (Google-style docstring)
        # Match "Args:" line followed by any number of indented lines.
        desc = re.sub(r"(?mi)^\s*Args?:\s*\n(?:[ \t].*\n)*", "", desc)

        # Also handle NumPy-style Parameters section
        # Parameters
        # ----------
        # x : int
        #     description
        desc = re.sub(
            r"(?mis)^\s*(Parameters|Arguments)\s*\n[-=]{3,}\s*\n(?:.*?\n(?=(?:^[^\s]|^\Z)))",
            "",
            desc,
        )

        # Clean up excessive blank lines
        desc = re.sub(r"\n{3,}", "\n\n", desc).strip()
        return desc

    @staticmethod
    def convert_oci_tool_call_to_langchain(tool_call: Any) -> ToolCall:
        """Convert an OCI tool call to a LangChain ToolCall."""

        def _get(obj: Any, *keys: str, default: Any = None) -> Any:
            for k in keys:
                if isinstance(obj, dict) and k in obj:
                    return obj[k]
                if hasattr(obj, k):
                    try:
                        return getattr(obj, k)
                    except Exception:
                        pass
            return default

        def _get_nested(obj: Any, path: tuple[str, ...], default: Any = None) -> Any:
            cur = obj
            for p in path:
                if isinstance(cur, dict) and p in cur:
                    cur = cur[p]
                elif hasattr(cur, p):
                    cur = getattr(cur, p)
                else:
                    return default
            return cur

        # If it's already a LangChain ToolCall, return as-is
        try:
            from langchain_core.messages import ToolCall as _LC_ToolCall  # type: ignore
            if isinstance(tool_call, _LC_ToolCall):
                return tool_call  # type: ignore[return-value]
        except Exception:
            pass

        # Try to extract fields from common OCI/OpenAI-like structures
        # Structure 1 (OpenAI-like): {"id": "...", "type": "function", "function": {"name": "...", "arguments": "{...}"}}
        name = (
            _get(tool_call, "name")
            or _get_nested(tool_call, ("function", "name"))
            or _get_nested(tool_call, ("tool", "name"))
        )

        raw_args = (
            _get(tool_call, "args", "arguments", "parameters")
            or _get_nested(tool_call, ("function", "arguments"))
            or _get_nested(tool_call, ("function", "args"))
            or _get_nested(tool_call, ("tool", "arguments"))
            or _get_nested(tool_call, ("tool", "args"))
        )

        call_id = (
            _get(tool_call, "id", "toolCallId", "call_id")
            or _get_nested(tool_call, ("function", "id"))
            or _get_nested(tool_call, ("tool", "id"))
        )

        # Normalize args to dict
        args: dict
        if isinstance(raw_args, str):
            parsed: dict | None = None
            try:
                parsed = json.loads(raw_args)
            except Exception:
                # Try to coerce simple "key=value" CSV style into dict if applicable
                try:
                    items = [kv.strip() for kv in raw_args.split(",")]
                    kv_dict: dict[str, Any] = {}
                    for it in items:
                        if "=" in it:
                            k, v = it.split("=", 1)
                            kv_dict[k.strip()] = v.strip()
                    if kv_dict:
                        parsed = kv_dict
                except Exception:
                    parsed = None
            args = parsed or {}
        elif isinstance(raw_args, dict):
            args = raw_args
        elif raw_args is None:
            args = {}
        else:
            # Attempt to convert via model_dump if it's a pydantic model / dataclass-like
            converted = None
            try:
                if hasattr(raw_args, "model_dump"):
                    converted = raw_args.model_dump()
                elif hasattr(raw_args, "dict"):
                    converted = raw_args.dict()
            except Exception:
                converted = None
            args = converted or {}

        if not name:
            # Fallback: some payloads might have "toolName"
            name = _get(tool_call, "toolName") or _get_nested(
                tool_call, ("tool", "toolName"))
        if not name:
            raise ValueError(
                "Unable to determine tool name from OCI tool call payload")

        # Construct LangChain ToolCall
        try:
            from langchain_core.messages import ToolCall as _LC_ToolCall  # type: ignore
            # type: ignore[return-value]
            return _LC_ToolCall(name=name, args=args, id=call_id)
        except Exception:
            # Fallback to previously imported alias if available
            # type: ignore[call-arg]
            return ToolCall(name=name, args=args, id=call_id)
