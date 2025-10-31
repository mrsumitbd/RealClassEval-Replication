from typing import Any
import sys
import json


class PrintingCallbackHandler:
    '''Handler for streaming text output and tool invocations to stdout.'''

    def __init__(self) -> None:
        '''Initialize handler.'''
        self._in_response = False
        self._last_tool_id = None

    def __call__(self, **kwargs: Any) -> None:
        '''Stream text output and tool invocations to stdout.
        Args:
            **kwargs: Callback event data including:
                - reasoningText (Optional[str]): Reasoning text to print if provided.
                - data (str): Text content to stream.
                - complete (bool): Whether this is the final chunk of a response.
                - current_tool_use (dict): Information about the current tool being used.
        '''
        reasoning_text = kwargs.get("reasoningText")
        if reasoning_text:
            sys.stdout.write(reasoning_text)
            if not str(reasoning_text).endswith("\n"):
                sys.stdout.write("\n")
            sys.stdout.flush()

        current_tool = kwargs.get("current_tool_use")
        if current_tool:
            tool_name = current_tool.get(
                "name") or current_tool.get("tool_name") or "tool"
            tool_args = current_tool.get(
                "args") or current_tool.get("input") or {}
            tool_id = (
                current_tool.get("id")
                or current_tool.get("call_id")
                or (tool_name, tuple(sorted(tool_args.items())) if isinstance(tool_args, dict) else str(tool_args))
            )
            if tool_id != self._last_tool_id:
                try:
                    args_str = json.dumps(tool_args, ensure_ascii=False)
                except Exception:
                    args_str = str(tool_args)
                sys.stdout.write(f"\n[Tool call] {tool_name} {args_str}\n")
                sys.stdout.flush()
                self._last_tool_id = tool_id

        data = kwargs.get("data")
        if data:
            sys.stdout.write(str(data))
            sys.stdout.flush()
            self._in_response = True

        if kwargs.get("complete"):
            if self._in_response and not (isinstance(data, str) and data.endswith("\n")):
                sys.stdout.write("\n")
                sys.stdout.flush()
            self._in_response = False
            self._last_tool_id = None
