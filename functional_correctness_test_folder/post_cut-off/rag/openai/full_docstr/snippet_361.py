
from __future__ import annotations

import json
import re
from typing import Any

from langchain.schema import ToolCall
from pydantic import BaseModel


class OCIUtils:
    """Utility functions for OCI Generative AI integration."""

    @staticmethod
    def is_pydantic_class(obj: Any) -> bool:
        """Check if an object is a Pydantic BaseModel subclass."""
        try:
            return issubclass(obj, BaseModel)
        except Exception:
            return False

    @staticmethod
    def remove_signature_from_tool_description(name: str, description: str) -> str:
        """
        Remove the tool signature and Args section from a tool description.

        The signature is typically prefixed to the description and followed
        by an Args section. This method strips the signature line and any
        Args section, returning the cleaned description.
        """
        # Remove the signature line (first line up to the first colon)
        parts = description.split("\n", 1)
        if len(parts) == 2 and ":" in parts[0]:
            description = parts[1]
        # Remove any Args section
        args_index = description.lower().find("args:")
        if args_index != -1:
            description = description[:args_index]
        return description.strip()

    @staticmethod
    def convert_oci_tool_call_to_langchain(tool_call: Any) -> ToolCall:
        """Convert an OCI tool call to a LangChain ToolCall."""
        # Extract name
        name = getattr(tool_call, "name", None)
        if name is None and isinstance(tool_call, dict):
            name = tool_call.get("name")
        if name is None:
            raise ValueError("OCI tool call does not contain a 'name' field")

        # Extract arguments
        args = getattr(tool_call, "arguments", None)
        if args is None and isinstance(tool_call, dict):
            args = tool_call.get("arguments")
        if args is None:
            args = {}

        # Ensure arguments are a JSON string
        if isinstance(args, dict):
            args_str = json.dumps(args)
        else:
            args_str = str(args)

        return ToolCall(name=name, arguments=args_str)
