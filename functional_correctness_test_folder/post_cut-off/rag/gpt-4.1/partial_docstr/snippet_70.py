import sys
from typing import Any, Optional


class PrintingCallbackHandler:
    '''Handler for streaming text output and tool invocations to stdout.'''

    def __init__(self) -> None:
        '''Initialize handler.'''
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
        reasoning_text: Optional[str] = kwargs.get("reasoningText")
        data: Optional[str] = kwargs.get("data")
        complete: bool = kwargs.get("complete", False)
        current_tool_use = kwargs.get("current_tool_use")

        if reasoning_text:
            print(reasoning_text, end="", flush=True)
        if data:
            print(data, end="", flush=True)
        if current_tool_use:
            print(f"\n[Tool use]: {current_tool_use}", flush=True)
        if complete:
            print(flush=True)
