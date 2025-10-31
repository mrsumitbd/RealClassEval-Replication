from typing import Any, Optional
import sys
import json


class PrintingCallbackHandler:
    '''Handler for streaming text output and tool invocations to stdout.'''

    def __init__(self) -> None:
        '''Initialize handler.'''
        self._last_tool: Optional[str] = None
        self._in_text_stream: bool = False

    def __call__(self, **kwargs: Any) -> None:
        '''Stream text output and tool invocations to stdout.
        Args:
            **kwargs: Callback event data including:
                - reasoningText (Optional[str]): Reasoning text to print if provided.
                - data (str): Text content to stream.
                - complete (bool): Whether this is the final chunk of a response.
                - current_tool_use (dict): Information about the current tool being used.
        '''
        reasoning = kwargs.get('reasoningText')
        if reasoning:
            sys.stdout.write(str(reasoning))
            sys.stdout.flush()
            self._in_text_stream = True

        tool = kwargs.get('current_tool_use') or {}
        if isinstance(tool, dict) and tool:
            name = tool.get('name') or tool.get('tool_name') or tool.get(
                'tool') or tool.get('id') or 'unknown'
            tool_input = (
                tool.get('input')
                or tool.get('args')
                or tool.get('arguments')
                or tool.get('tool_input')
                or {}
            )
            if name != self._last_tool:
                if self._in_text_stream:
                    sys.stdout.write('\n')
                    self._in_text_stream = False
                try:
                    input_repr = json.dumps(tool_input, ensure_ascii=False)
                except Exception:
                    input_repr = str(tool_input)
                sys.stdout.write(f'[tool call] {name} {input_repr}\n')
                sys.stdout.flush()
                self._last_tool = name

        data = kwargs.get('data')
        if data is not None:
            sys.stdout.write(str(data))
            sys.stdout.flush()
            self._in_text_stream = True

        if kwargs.get('complete'):
            sys.stdout.write('\n')
            sys.stdout.flush()
            self._in_text_stream = False
            self._last_tool = None
