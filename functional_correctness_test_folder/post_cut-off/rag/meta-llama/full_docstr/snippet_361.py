
from typing import Any
from pydantic import BaseModel
from langchain_core.tools import ToolCall


class OCIUtils:
    """Utility functions for OCI Generative AI integration."""

    @staticmethod
    def is_pydantic_class(obj: Any) -> bool:
        """Check if an object is a Pydantic BaseModel subclass."""
        return isinstance(obj, type) and issubclass(obj, BaseModel)

    @staticmethod
    def remove_signature_from_tool_description(name: str, description: str) -> str:
        """
        Remove the tool signature and Args section from a tool description.

        The signature is typically prefixed to the description and followed
        by an Args section.
        """
        lines = description.splitlines()
        # Find the index of the first line that doesn't start with a parameter or a signature part
        idx = next((i for i, line in enumerate(lines) if not line.startswith(
            ('    ', 'Args:')) and line.strip()), None)
        if idx is not None:
            # Check if 'Args:' is present after the signature
            args_idx = next((i for i, line in enumerate(
                lines[idx:], start=idx) if line.strip() == 'Args:'), None)
            if args_idx is not None:
                return '\n'.join(lines[args_idx+1:]).strip()
            else:
                return '\n'.join(lines[idx:]).strip()
        return description.strip()

    @staticmethod
    def convert_oci_tool_call_to_langchain(tool_call: Any) -> ToolCall:
        """Convert an OCI tool call to a LangChain ToolCall."""
        return ToolCall(
            name=tool_call.name,
            args=tool_call.arguments,
            id=tool_call.id
        )
