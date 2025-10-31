
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
        reasoning_text: Optional[str] = kwargs.get('reasoningText')
        data: Optional[str] = kwargs.get('data')
        complete: bool = kwargs.get('complete', False)
        current_tool_use: Optional[dict] = kwargs.get('current_tool_use')

        if reasoning_text is not None:
            print(f"[Reasoning] {reasoning_text}")

        if data is not None:
            print(data, end='' if not complete else '\n', flush=True)

        if current_tool_use is not None:
            print(f"[Tool Invocation] {current_tool_use}")
