
import sys
from typing import Any, Optional


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
        reasoning: Optional[str] = kwargs.get("reasoningText")
        data: str = kwargs.get("data", "")
        complete: bool = kwargs.get("complete", False)
        current_tool_use: Optional[dict] = kwargs.get("current_tool_use")

        # Print reasoning text if present
        if reasoning:
            print(reasoning, flush=True)

        # Print tool usage information if present
        if current_tool_use:
            # Common keys that might hold tool name and arguments
            tool_name = (
                current_tool_use.get("name")
                or current_tool_use.get("tool_name")
                or current_tool_use.get("tool")
                or "unknown tool"
            )
            tool_args = (
                current_tool_use.get("arguments")
                or current_tool_use.get("args")
                or current_tool_use.get("parameters")
                or {}
            )
            print(f"Using tool: {tool_name}", flush=True)
            if tool_args:
                # Pretty‑print arguments if they are a dict or list
                if isinstance(tool_args, (dict, list)):
                    print(f"Tool arguments: {tool_args}", flush=True)
                else:
                    print(f"Tool arguments: {tool_args}", flush=True)

        # Stream the data chunk
        if data:
            # Avoid adding an extra newline; let the caller decide
            print(data, end="", flush=True)

        # If this is the final chunk, finish the line
        if complete:
            print()
