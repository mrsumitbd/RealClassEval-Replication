
from typing import Any


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
        reasoning_text = kwargs.get('reasoningText')
        if reasoning_text is not None:
            print(f'Reasoning: {reasoning_text}')

        data = kwargs.get('data')
        if data is not None:
            print(data, end='', flush=True)

        complete = kwargs.get('complete', False)
        if complete:
            print()  # Newline after complete response

        current_tool_use = kwargs.get('current_tool_use')
        if current_tool_use is not None:
            print(f'Tool: {current_tool_use.get("name", "Unknown")}')
            print(f'Tool Input: {current_tool_use.get("input", {})}')
