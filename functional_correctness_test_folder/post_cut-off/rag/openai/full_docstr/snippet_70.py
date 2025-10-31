
from __future__ import annotations

from typing import Any, Dict, Optional
import sys


class PrintingCallbackHandler:
    """Handler for streaming text output and tool invocations to stdout."""

    def __init__(self) -> None:
        """Initialize handler."""
        # No state needed for this simple handler
        pass

    def __call__(self, **kwargs: Any) -> None:
        """
        Stream text output and tool invocations to stdout.

        Parameters
        ----------
        **kwargs : Any
            Callback event data including:
                - reasoningText (Optional[str]): Reasoning text to print if provided.
                - data (str): Text content to stream.
                - complete (bool): Whether this is the final chunk of a response.
                - current_tool_use (dict): Information about the current tool being used.
        """
        # Extract values with defaults
        reasoning_text: Optional[str] = kwargs.get("reasoningText")
        data: Optional[str] = kwargs.get("data")
        complete: bool = kwargs.get("complete", False)
        current_tool_use: Optional[Dict[str, Any]
                                   ] = kwargs.get("current_tool_use")

        # Print reasoning text if present
        if reasoning_text:
            # Avoid adding a newline if the caller will add it later
            sys.stdout.write(reasoning_text)
            sys.stdout.flush()

        # Print streamed data
        if data:
            sys.stdout.write(data)
            sys.stdout.flush()

        # If this is the final chunk, add a newline for readability
        if complete:
            sys.stdout.write("\n")
            sys.stdout.flush()

        # Print tool invocation details if provided
        if current_tool_use:
            # Build a readable representation of the tool usage
            tool_name = current_tool_use.get("name") if isinstance(
                current_tool_use, dict) else None
            tool_args = current_tool_use.get("arguments") if isinstance(
                current_tool_use, dict) else None
            tool_output = current_tool_use.get("output") if isinstance(
                current_tool_use, dict) else None

            # Format the tool information
            parts = []
            if tool_name:
                parts.append(f"Tool: {tool_name}")
            if tool_args is not None:
                parts.append(f"Args: {tool_args}")
            if tool_output is not None:
                parts.append(f"Output: {tool_output}")

            if parts:
                sys.stdout.write("\n" + " | ".join(parts) + "\n")
                sys.stdout.flush()
