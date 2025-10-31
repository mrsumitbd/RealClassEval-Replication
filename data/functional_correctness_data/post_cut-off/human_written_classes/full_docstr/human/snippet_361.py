import uuid
import re
from typing import Any, Callable, Dict, Iterator, List, Literal, Mapping, Optional, Sequence, Set, Type, Union
import json
from langchain_core.messages import AIMessage, AIMessageChunk, BaseMessage, ChatMessage, HumanMessage, SystemMessage, ToolCall, ToolMessage
from pydantic import BaseModel, ConfigDict

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
        description = re.sub(f'^{name}\\(.*?\\) -(?:> \\w+? -)? ', '', description)
        description = re.sub('(?s)(?:\\n?\\n\\s*?)?Args:.*$', '', description)
        return description

    @staticmethod
    def convert_oci_tool_call_to_langchain(tool_call: Any) -> ToolCall:
        """Convert an OCI tool call to a LangChain ToolCall."""
        return ToolCall(name=tool_call.name, args=json.loads(tool_call.arguments) if 'arguments' in tool_call.attribute_map else tool_call.parameters, id=tool_call.id if 'id' in tool_call.attribute_map else uuid.uuid4().hex[:])