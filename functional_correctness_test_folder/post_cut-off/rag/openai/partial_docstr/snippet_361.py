
from __future__ import annotations

from typing import Any
import json

try:
    from pydantic import BaseModel
except Exception:  # pragma: no cover
    BaseModel = None  # type: ignore

try:
    from langchain.schema import ToolCall
except Exception:  # pragma: no cover
    ToolCall = None  # type: ignore


class OCIUtils:
    """Utility functions for OCI Generative AI integration."""

    @staticmethod
    def is_pydantic_class(obj: Any) -> bool:
        """Check if an object is a Pydantic BaseModel subclass."""
        if BaseModel is None:
            return False
        return isinstance(obj, type) and issubclass(obj, BaseModel)

    @staticmethod
    def remove_signature_from_tool_description(name: str, description: str) -> str:
        """
        Remove the tool signature and Args section from a tool description.
        The signature is typically prefixed to the description and followed
        by an Args section.
        """
        # Remove the signature (everything up to the first newline after the
        # closing parenthesis of the signature).
        sig_end = description.find("):")
        if sig_end != -1:
            # Find the next newline after the signature
            nl = description.find("\n", sig_end)
            if nl != -1:
                description = description[nl + 1:]
            else:
                description = description[sig_end + 2:]

        # Remove the Args section if present
        args_start = description.lower().find("\nargs:")
        if args_start == -1:
            args_start = description.lower().find("\narguments:")
        if args_start != -1:
            description = description[:args_start]

        return description.strip()

    @staticmethod
    def convert_oci_tool_call_to_langchain(tool_call: Any) -> ToolCall:
        """Convert an OCI tool call to a LangChain ToolCall."""
        if ToolCall is None:
            raise RuntimeError("langchain.schema.ToolCall is not available")

        # OCI tool calls are expected to have `name` and `arguments` attributes.
        name = getattr(tool_call, "name", None)
        if name is None:
            raise ValueError("OCI tool call missing 'name' attribute")

        args = getattr(tool_call, "arguments", None)
        if args is None:
            raise ValueError("OCI tool call missing 'arguments' attribute")

        # If arguments are already a JSON string, use as is; otherwise dump to JSON.
        if isinstance(args, str):
            arguments_json = args
        else:
            arguments_json = json.dumps(args, ensure_ascii=False)

        return ToolCall(name=name, arguments=arguments_json)
