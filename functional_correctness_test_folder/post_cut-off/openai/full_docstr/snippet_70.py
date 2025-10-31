
from __future__ import annotations

from typing import Any, Optional
import sys


class PrintingCallbackHandler:
    '''Handler for streaming text output and tool invocations to stdout.'''

    def __init__(self) -> None:
        '''Initialize handler.'''
        # No internal state needed for this simple handler
        pass

    def __call__(self, **kwargs: Any) -> None:
        '''Stream text output and tool invocations to stdout.
        Args:
            **kwargs: Callback event data including:
                - reasoningText (Optional[str]): Reasoning text to print if provided.
                - data (str): Text content to stream.
                - complete (bool): Whether this is the final chunk of a response.
                - current_tool_use (dict): Information about the current tool being used.
        '''
        reasoning_text: Optional[str] = kwargs.get('reasoningText')
        data: str = kwargs.get('data', '')
        complete: bool = kwargs.get('complete', False)
        current_tool_use: Optional[dict] = kwargs.get('current_tool_use')

        # Print reasoning text if present
        if reasoning_text:
            sys.stdout.write(reasoning_text)
            sys.stdout.flush()

        # Print streamed data
        if data:
            sys.stdout.write(data)
            sys.stdout.flush()

        # Print tool invocation details if present
        if current_tool_use:
            tool_name = current_tool_use.get('name', 'unknown')
            tool_args = current_tool_use.get('arguments', {})
            sys.stdout.write(
                f"\n[Tool: {tool_name} invoked with args: {tool_args}]\n")
            sys.stdout.flush()

        # If this is the final chunk, add a newline for readability
        if complete:
            sys.stdout.write('\n')
            sys.stdout.flush()
