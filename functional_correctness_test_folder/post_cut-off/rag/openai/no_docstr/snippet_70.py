
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

        Args:
            **kwargs: Callback event data including:
                - reasoningText (Optional[str]): Reasoning text to print if provided.
                - data (str): Text content to stream.
                - complete (bool): Whether this is the final chunk of a response.
                - current_tool_use (dict): Information about the current tool being used.
        """
        reasoning_text: Optional[str] = kwargs.get("reasoningText")
        data: Optional[str] = kwargs.get("data")
        complete: bool = kwargs.get("complete", False)
        current_tool_use: Optional[Dict[str, Any]
                                   ] = kwargs.get("current_tool_use")

        # Print reasoning text if present
        if reasoning_text:
            sys.stdout.write(reasoning_text)
            sys.stdout.flush()

        # Print streamed data if present
        if data:
            sys.stdout.write(data)
            sys.stdout.flush()

        # Print tool invocation details if present
        if current_tool_use:
            # Try to format nicely
            tool_name = current_tool_use.get(
                "name") or current_tool_use.get("tool_name")
            arguments = current_tool_use.get(
                "arguments") or current_tool_use.get("args")
            if tool_name is not None:
                sys.stdout.write(f"\n[Tool] {tool_name}")
                if arguments is not None:
                    sys.stdout.write(f" with arguments: {arguments}")
            else:
                # Fallback to raw dict representation
                sys.stdout.write(f"\n[Tool] {current_tool_use}")
            sys.stdout.flush()

        # If this is the final chunk, add a newline for cleanliness
        if complete:
            sys.stdout.write("\n")
            sys.stdout.flush()
