from typing import Any, Optional
import sys
import json


class PrintingCallbackHandler:
    '''Handler for streaming text output and tool invocations to stdout.'''

    def __init__(self) -> None:
        '''Initialize handler.'''
        self._last_tool_name: Optional[str] = None
        self._in_tool: bool = False

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
        if isinstance(reasoning_text, str) and reasoning_text:
            sys.stdout.write(reasoning_text)
            sys.stdout.flush()

        current_tool = kwargs.get('current_tool_use')
        if isinstance(current_tool, dict) and current_tool:
            name = current_tool.get('name') or current_tool.get(
                'tool_name') or current_tool.get('type') or 'tool'
            params = (
                current_tool.get('input') or
                current_tool.get('parameters') or
                current_tool.get('args') or
                current_tool.get('arguments')
            )
            if name != self._last_tool_name:
                # Start of a new tool invocation
                sys.stdout.write(f'\n[Tool: {name}]')
                if params is not None:
                    try:
                        rendered = params if isinstance(
                            params, str) else json.dumps(params, ensure_ascii=False)
                    except Exception:
                        rendered = str(params)
                    sys.stdout.write(f' {rendered}')
                sys.stdout.write('\n')
                sys.stdout.flush()
                self._last_tool_name = name
                self._in_tool = True

        data = kwargs.get('data')
        if isinstance(data, str) and data:
            sys.stdout.write(data)
            sys.stdout.flush()

        if kwargs.get('complete') is True:
            sys.stdout.write('\n')
            sys.stdout.flush()
            # Reset tool tracking on completion of a response
            self._in_tool = False
            self._last_tool_name = None
