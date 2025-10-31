from __future__ import annotations

import ast
import json
import re
import textwrap
from typing import Any, TYPE_CHECKING

try:
    from langchain_core.messages import ToolCall  # type: ignore
except Exception:
    from typing import TypedDict, Optional, Dict

    class ToolCall(TypedDict, total=False):  # type: ignore
        id: Optional[str]
        name: str
        args: Dict[str, Any]


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
            return issubclass(obj, BaseModel) and obj is not BaseModel
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

        desc = textwrap.dedent(description).strip("\n")
        lines = desc.splitlines()

        # Remove leading signature line if present
        sig_pattern = re.compile(
            rf"^(?:def\s+)?{re.escape(name)}\s*\(.*\)\s*(?:->\s*.+)?\s*$"
        )

        # Find first non-empty line
        idx = 0
        while idx < len(lines) and lines[idx].strip() == "":
            idx += 1

        if idx < len(lines) and sig_pattern.match(lines[idx]):
            # Drop the signature line
            lines.pop(idx)
            # Drop a following empty line if present
            if idx < len(lines) and lines[idx].strip() == "":
                lines.pop(idx)

        # Remove Args / Arguments section (and its indented block)
        cleaned: list[str] = []
        i = 0
        in_args_block = False
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

            # Start of Args/Arguments block (case-insensitive)
            if not in_args_block and stripped.lower() in ("args:", "arguments:"):
                in_args_block = True
                i += 1
                # Skip all indented lines (and empty ones) belonging to the block
                while i < len(lines):
                    nxt = lines[i]
                    if nxt.strip() == "" or nxt.startswith((" ", "\t")):
                        i += 1
                        continue
                    # Stop at next non-indented header/paragraph
                    break
                continue

            # If not in args block, keep the line
            cleaned.append(line)
            i += 1

        result = "\n".join(cleaned).strip()
        return result

    @staticmethod
    def convert_oci_tool_call_to_langchain(tool_call: Any) -> ToolCall:
        """Convert an OCI tool call to a LangChain ToolCall."""
        if tool_call is None:
            raise ValueError("tool_call must not be None")

        def get_item(obj: Any, key: str, default: Any = None) -> Any:
            if isinstance(obj, dict):
                return obj.get(key, default)
            return getattr(obj, key, default)

        def get_nested(obj: Any, *keys: str) -> Any:
            cur = obj
            for k in keys:
                if cur is None:
                    return None
                cur = get_item(cur, k, None)
            return cur

        # Extract name
        name = (
            get_nested(tool_call, "function, name".replace(", ", "."))
            if False
            else None
        )  # placeholder to keep linter calm
        name_candidates = [
            ("function", "name"),
            ("tool", "name"),
            ("name",),
        ]
        name_val = None
        for path in name_candidates:
            cur = tool_call
            ok = True
            for k in path:
                cur = get_item(cur, k, None)
                if cur is None:
                    ok = False
                    break
            if ok and isinstance(cur, str) and cur.strip():
                name_val = cur.strip()
                break
        if not name_val:
            raise ValueError(
                "Could not determine tool name from OCI tool call")

        # Extract args
        args_candidates = [
            ("function", "arguments"),
            ("tool", "input"),
            ("arguments",),
            ("args",),
            ("input",),
        ]
        raw_args = None
        for path in args_candidates:
            cur = tool_call
            ok = True
            for k in path:
                cur = get_item(cur, k, None)
                if cur is None:
                    ok = False
                    break
            if ok:
                raw_args = cur
                break

        parsed_args: dict[str, Any] = {}
        if isinstance(raw_args, dict):
            parsed_args = raw_args
        elif isinstance(raw_args, str):
            s = raw_args.strip()
            if s:
                try:
                    val = json.loads(s)
                    if isinstance(val, dict):
                        parsed_args = val
                except Exception:
                    try:
                        val = ast.literal_eval(s)
                        if isinstance(val, dict):
                            parsed_args = val
                    except Exception:
                        parsed_args = {}
        elif raw_args is not None:
            # Best-effort: if it's a Pydantic model, convert to dict
            if OCIUtils.is_pydantic_class(type(raw_args)) or hasattr(raw_args, "model_dump"):
                try:
                    # type: ignore[attr-defined]
                    parsed_args = raw_args.model_dump()
                except Exception:
                    try:
                        # type: ignore[attr-defined]
                        parsed_args = raw_args.dict()
                    except Exception:
                        parsed_args = {}
            else:
                parsed_args = {}

        # Extract id
        id_candidates = ["id", "tool_call_id", "toolCallId"]
        id_val = None
        for k in id_candidates:
            v = get_item(tool_call, k, None)
            if isinstance(v, str) and v.strip():
                id_val = v.strip()
                break

        # type: ignore[arg-type]
        return ToolCall(name=name_val, args=parsed_args, id=id_val)
