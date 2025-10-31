
from __future__ import annotations

import json
from typing import Any

try:
    from pydantic import BaseModel
except Exception:
    BaseModel = None

try:
    from langchain.schema import ToolCall
except Exception:
    # Minimal fallback definition if langchain is not installed
    class ToolCall:
        def __init__(self, name: str, args: dict):
            self.name = name
            self.args = args

        def __repr__(self):
            return f"ToolCall(name={self.name!r}, args={self.args!r})"


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
        # Remove the signature (everything up to the first closing parenthesis)
        sig_end = description.find("):")
        if sig_end != -1:
            description = description[sig_end + 2:].lstrip()
        # Remove the Args section if present
        args_start = description.lower().find("\nargs:")
        if args_start != -1:
            description = description[:args_start].rstrip()
        return description

    @staticmethod
    def convert_oci_tool_call_to_langchain(tool_call: Any) -> ToolCall:
        """Convert an OCI tool call to a LangChain ToolCall."""
        # OCI tool call is expected to be a dict with 'name' and 'arguments'
        if not isinstance(tool_call, dict):
            raise TypeError("OCI tool call must be a dict")
        name = tool_call.get("name")
        if name is None:
            raise ValueError("OCI tool call missing 'name' field")
        arguments = tool_call.get("arguments", {})
        # If arguments is a JSON string, parse it
        if isinstance(arguments, str):
            try:
                arguments = json.loads(arguments)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON arguments: {exc}") from exc
        if not isinstance(arguments, dict):
            raise TypeError(
                "OCI tool call 'arguments' must be a dict or JSON string")
        return ToolCall(name=name, args=arguments)
