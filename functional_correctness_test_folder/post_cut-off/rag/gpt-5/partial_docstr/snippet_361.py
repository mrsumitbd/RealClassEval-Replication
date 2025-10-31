from __future__ import annotations

import ast
import json
import re
from dataclasses import asdict, is_dataclass
from typing import Any, Dict

try:
    from langchain_core.messages import ToolCall  # type: ignore
except Exception:
    from typing import TypedDict, Optional

    class ToolCall(TypedDict, total=False):
        name: str
        args: Dict[str, Any]
        id: Optional[str]


class OCIUtils:
    """Utility functions for OCI Generative AI integration."""

    @staticmethod
    def is_pydantic_class(obj: Any) -> bool:
        """Check if an object is a Pydantic BaseModel subclass."""
        try:
            from pydantic import BaseModel  # type: ignore
        except Exception:
            return False
        try:
            return isinstance(obj, type) and issubclass(obj, BaseModel)
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

        lines = description.splitlines()

        def is_signature_line(line: str) -> bool:
            s = line.strip()
            if not s:
                return False
            if s.startswith("def ") and name in s and "(" in s and ")" in s:
                return True
            if s.startswith(f"{name}(") and ")" in s:
                return True
            if s.startswith(name) and "(" in s and ")" in s:
                return True
            return False

        # Drop a leading signature line if present (within the first two lines)
        for idx in range(min(2, len(lines))):
            if is_signature_line(lines[idx]):
                lines = lines[idx + 1:]
                break

        # Trim leading empty lines after removing signature
        while lines and not lines[0].strip():
            lines.pop(0)

        # Remove Args section if present
        i = 0
        out: list[str] = []
        in_args = False
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

            if not in_args and stripped.lower().startswith("args:"):
                in_args = True
                i += 1
                continue

            if in_args:
                # Skip lines belonging to Args section.
                # Args section typically consists of indented lines, bullets, or param: desc pairs.
                if (
                    not stripped
                    or line.startswith((" ", "\t"))
                    or stripped.startswith(("-", "*"))
                    or re.match(r"^[A-Za-z_][A-Za-z0-9_]*\s*:\s*", stripped) is not None
                ):
                    i += 1
                    continue

                # If we encounter a non-indented, capitalized section header like "Returns:", stop skipping.
                if re.match(r"^[A-Z][A-Za-z ]*:\s*$", stripped):
                    in_args = False
                    out.append(line)
                    i += 1
                    continue

                # Any other non-indented content ends Args, include it
                in_args = False
                out.append(line)
                i += 1
                continue

            out.append(line)
            i += 1

        result = "\n".join(out).strip("\n")
        return result

    @staticmethod
    def convert_oci_tool_call_to_langchain(tool_call: Any) -> ToolCall:
        """Convert an OCI tool call to a LangChain ToolCall."""

        def _get(value: Any, key: str, default: Any = None) -> Any:
            if isinstance(value, dict):
                return value.get(key, default)
            return getattr(value, key, default)

        def _to_args_dict(value: Any) -> Dict[str, Any]:
            if value is None:
                return {}
            if isinstance(value, dict):
                return value
            if isinstance(value, str):
                s = value.strip()
                if not s:
                    return {}
                # Try JSON then Python literal
                try:
                    loaded = json.loads(s)
                    return loaded if isinstance(loaded, dict) else {}
                except Exception:
                    try:
                        loaded = ast.literal_eval(s)
                        return loaded if isinstance(loaded, dict) else {}
                    except Exception:
                        return {}
            # Pydantic instance (v2 model_dump / v1 dict)
            try:
                from pydantic import BaseModel  # type: ignore

                if isinstance(value, BaseModel):
                    if hasattr(value, "model_dump"):
                        return value.model_dump()  # type: ignore[attr-defined]
                    if hasattr(value, "dict"):
                        return value.dict()  # type: ignore[attr-defined]
            except Exception:
                pass
            # Dataclass instance
            if is_dataclass(value):
                try:
                    return asdict(value)
                except Exception:
                    return {}
            # Fallback for simple namespace-like objects
            if hasattr(value, "__dict__"):
                try:
                    d = dict(value.__dict__)
                    return d if isinstance(d, dict) else {}
                except Exception:
                    return {}
            return {}

        # Normalize OCI/OpenAI-compatible tool call structures to LangChain ToolCall
        func_block = _get(tool_call, "function", None)
        if func_block is not None:
            name = _get(func_block, "name")
            args_val = _get(func_block, "arguments", None)
            if args_val is None:
                args_val = _get(func_block, "args", None)
            if args_val is None:
                args_val = _get(func_block, "parameters", None)
            call_id = _get(tool_call, "id", None)
        else:
            name = _get(tool_call, "name")
            args_val = _get(tool_call, "arguments", None)
            if args_val is None:
                args_val = _get(tool_call, "args", None)
            if args_val is None:
                args_val = _get(tool_call, "parameters", None)
            call_id = _get(tool_call, "id", None)

        if not name:
            raise ValueError("Tool call does not contain a function name.")

        args = _to_args_dict(args_val)

        # type: ignore[call-arg]
        return ToolCall(name=name, args=args, id=call_id)
