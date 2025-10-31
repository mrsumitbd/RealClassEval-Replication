from typing import Any, Optional, Set
import json


class PrintingCallbackHandler:
    '''Handler for streaming text output and tool invocations to stdout.'''

    def __init__(self) -> None:
        '''Initialize handler.'''
        self._line_open: bool = False
        self._seen_tools: Set[str] = set()

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
            print(str(reasoning), end='', flush=True)
            self._line_open = True

        tool_info = kwargs.get('current_tool_use') or {}
        if isinstance(tool_info, dict) and tool_info:
            tool_id = str(
                tool_info.get('id')
                or tool_info.get('tool_use_id')
                or tool_info.get('name')
                or ''
            )
            if tool_id and tool_id not in self._seen_tools:
                name = tool_info.get('name') or tool_id
                args = tool_info.get('input')
                if args is None:
                    args = tool_info.get('arguments', tool_info.get('args'))
                try:
                    if isinstance(args, (dict, list)):
                        arg_str = json.dumps(args, ensure_ascii=False)
                    elif args is not None:
                        arg_str = str(args)
                    else:
                        arg_str = None
                except Exception:
                    arg_str = str(args)
                prefix = '\n' if self._line_open else ''
                if arg_str:
                    print(
                        f'{prefix}Using tool: {name} with input: {arg_str}', flush=True)
                else:
                    print(f'{prefix}Using tool: {name}', flush=True)
                self._seen_tools.add(tool_id)
                self._line_open = False

            output = tool_info.get('output') or tool_info.get(
                'result') or tool_info.get('response')
            if output not in (None, ''):
                print(f'Tool output: {output}', flush=True)
                self._line_open = False

        data = kwargs.get('data')
        if data:
            print(str(data), end='', flush=True)
            self._line_open = True

        if kwargs.get('complete'):
            if self._line_open:
                print(flush=True)
            self._line_open = False
