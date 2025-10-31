
from typing import Any
from langchain.schema.messages import ToolCall


class OCIUtils:
    """Utility functions for OCI Generative AI integration."""

    @staticmethod
    def is_pydantic_class(obj: Any) -> bool:
        """Check if an object is a Pydantic BaseModel subclass."""
        try:
            from pydantic import BaseModel
            return isinstance(obj, type) and issubclass(obj, BaseModel)
        except ImportError:
            return False

    @staticmethod
    def remove_signature_from_tool_description(name: str, description: str) -> str:
        """
        Remove the tool signature and Args section from a tool description.
        The signature is typically prefixed to the description and followed
        by an Args section.
        """
        # Remove signature (e.g., "tool_name(arg1: type, arg2: type)")
        if description.startswith(name + "("):
            description = description.split("\n\n", 1)[-1]
        # Remove Args section if present
        if "Args:" in description:
            description = description.split("Args:", 1)[0].strip()
        return description

    @staticmethod
    def convert_oci_tool_call_to_langchain(tool_call: Any) -> ToolCall:
        """Convert an OCI tool call to a LangChain ToolCall."""
        return ToolCall(
            name=tool_call.name,
            args=tool_call.arguments,
            id=tool_call.id if hasattr(tool_call, "id") else None
        )
