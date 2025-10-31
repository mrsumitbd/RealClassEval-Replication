
from __future__ import annotations

import json
import re
from typing import Any

from langchain.schema import ToolCall
from pydantic import BaseModel


class OCIUtils:
    @staticmethod
    def is_pydantic_class(obj: Any) -> bool:
        """Check if an object is a Pydantic BaseModel subclass."""
        # Accept both class objects and instances
        if isinstance(obj, type):
            return issubclass(obj, BaseModel)
        return isinstance(obj, BaseModel)

    @staticmethod
    def remove_signature_from_tool_description(name: str, description: str) -> str:
        """
        Remove any signature block from a tool description.

        The function looks for common signature markers such as
        ``signature:`` or ``Signature:`` and strips everything from that
        marker to the end of the string. If no marker is found, the
        original description is returned unchanged.
        """
        # Regex to find "signature:" or "Signature:" (case‑insensitive)
        pattern = re.compile(r'\s*signature\s*:\s*.*', re.IGNORECASE)
        # Split on the first occurrence of the pattern
        parts = pattern.split(description, maxsplit=1)
        return parts[0].strip() if parts else description.strip()

    @staticmethod
    def convert_oci_tool_call_to_langchain(tool_call: Any) -> ToolCall:
        """
        Convert an OCI tool call to a LangChain ToolCall.

        The OCI tool call is expected to expose at least the following
        attributes:
            - name: the name of the tool
            - arguments: a dict of arguments
            - id (optional): an identifier for the call

        The resulting LangChain ToolCall will contain:
            - name: same as OCI
            - args: JSON string of the arguments
            - id: same as OCI if present, otherwise None
        """
        name = getattr(tool_call, "name", None)
        if name is None:
            raise ValueError("OCI tool call must have a 'name' attribute")

        arguments = getattr(tool_call, "arguments", {})
        if not isinstance(arguments, dict):
            raise TypeError("OCI tool call 'arguments' must be a dict")

        args_json = json.dumps(arguments, ensure_ascii=False)

        call_id = getattr(tool_call, "id", None)

        return ToolCall(name=name, args=args_json, id=call_id)
