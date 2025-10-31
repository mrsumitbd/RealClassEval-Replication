
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
        # Find the index of the first line that doesn't start with a parameter or a signature keyword
        for i, line in enumerate(lines):
            if not (line.strip().startswith(':param') or line.strip().startswith(name)):
                break
        # Find the index of the 'Args:' section
        args_index = next((i for i, line in enumerate(
            lines) if line.strip().lower() == 'args:'), len(lines))
        # Return the description without the signature and Args section
        return '\n'.join(lines[i:args_index]).strip()

    @staticmethod
    def convert_oci_tool_call_to_langchain(tool_call: Any) -> ToolCall:
        """Convert an OCI tool call to a LangChain ToolCall."""
        return ToolCall(
            name=tool_call.name,
            args=tool_call.arguments,
            id=tool_call.id
        )
