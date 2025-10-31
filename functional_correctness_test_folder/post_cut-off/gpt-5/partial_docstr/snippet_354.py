from __future__ import annotations

from typing import Any, Optional, Mapping
import json


class EventRenderer:
    '''Stateful renderer that groups function calls with their responses.'''

    def __init__(self) -> None:
        '''Initialize the event renderer.'''
        self._pending_function_call: Optional[Any] = None

    def render_event(self, obj: 'Event', console: 'Console') -> None:
        # Normalize mapping-like events
        if isinstance(obj, Mapping):
            evt_type = obj.get('type') or obj.get('event') or obj.get('kind')
            if evt_type == 'function_call':
                self._flush_pending_function_call(console)
                self._pending_function_call = obj
                return
            if evt_type in ('function_response', 'function_result', 'tool_result', 'tool_response'):
                response = obj.get('response') or obj.get(
                    'data') or obj.get('result') or obj
                if self._pending_function_call is not None:
                    self._render_function_call_group(
                        self._pending_function_call, response, console)
                    self._pending_function_call = None
                else:
                    # No pending call; just render the response
                    console.print(self._format_response(response))
                return
            # Other events: flush pending and print
            self._flush_pending_function_call(console)
            # Try to show a readable representation
            content = obj.get('content') or obj.get('message') or obj
            console.print(content)
            return

        # Object-like events
        evt_type = getattr(obj, 'type', None) or getattr(
            obj, 'event', None) or getattr(obj, 'kind', None)

        # If the object itself looks like a function call
        if self._looks_like_function_call(obj) or evt_type == 'function_call':
            self._flush_pending_function_call(console)
            self._pending_function_call = obj
            return

        # If the object looks like a function response
        if evt_type in ('function_response', 'function_result', 'tool_result', 'tool_response') or self._looks_like_function_response(obj):
            response = self._extract_response_payload(obj)
            if self._pending_function_call is not None:
                self._render_function_call_group(
                    self._pending_function_call, response, console)
                self._pending_function_call = None
            else:
                console.print(self._format_response(response))
            return

        # Generic event: flush pending and print
        self._flush_pending_function_call(console)
        content = getattr(obj, 'content', None) or getattr(
            obj, 'message', None) or str(obj)
        console.print(content)

    def _flush_pending_function_call(self, console: 'Console') -> None:
        if self._pending_function_call is None:
            return
        fc = self._pending_function_call
        name = self._extract_function_name(fc)
        args = self._extract_function_args(fc)
        console.print(f"Function call: {name}")
        console.print(f"Arguments: {args}")
        self._pending_function_call = None

    def _render_function_call_group(self, function_call: 'FunctionCall', response: dict[str, Any], console: 'Console') -> None:
        '''Render function call and response together in a grouped panel.'''
        name = self._extract_function_name(function_call)
        args = self._extract_function_args(function_call)
        console.print(f"Function call: {name}")
        console.print(f"Arguments: {args}")
        console.print("Response:")
        console.print(self._format_response(response))

    # Helpers

    def _looks_like_function_call(self, obj: Any) -> bool:
        if isinstance(obj, Mapping):
            return obj.get('type') == 'function_call' or ('name' in obj and 'arguments' in obj)
        return hasattr(obj, 'name') and hasattr(obj, 'arguments')

    def _looks_like_function_response(self, obj: Any) -> bool:
        if isinstance(obj, Mapping):
            t = obj.get('type')
            return t in ('function_response', 'function_result', 'tool_result', 'tool_response') or 'response' in obj or 'result' in obj or 'data' in obj
        return hasattr(obj, 'response') or hasattr(obj, 'result') or hasattr(obj, 'data')

    def _extract_function_name(self, function_call: Any) -> str:
        if isinstance(function_call, Mapping):
            return str(function_call.get('name') or function_call.get('function') or 'unknown')
        return str(getattr(function_call, 'name', None) or getattr(function_call, 'function', None) or 'unknown')

    def _extract_function_args(self, function_call: Any) -> str:
        args = None
        if isinstance(function_call, Mapping):
            args = function_call.get('arguments') or function_call.get(
                'args') or function_call.get('parameters')
        else:
            args = getattr(function_call, 'arguments', None) or getattr(
                function_call, 'args', None) or getattr(function_call, 'parameters', None)
        return self._format_json_like(args)

    def _extract_response_payload(self, obj: Any) -> Any:
        if isinstance(obj, Mapping):
            return obj.get('response') or obj.get('result') or obj.get('data') or obj
        return getattr(obj, 'response', None) or getattr(obj, 'result', None) or getattr(obj, 'data', None) or obj

    def _format_response(self, response: Any) -> str:
        return self._format_json_like(response)

    def _format_json_like(self, data: Any) -> str:
        # Try to pretty print as JSON if appropriate
        try:
            if isinstance(data, str):
                data = data.strip()
                if data.startswith('{') or data.startswith('['):
                    parsed = json.loads(data)
                    return json.dumps(parsed, indent=2, ensure_ascii=False)
                return data
            if isinstance(data, (dict, list, tuple)):
                return json.dumps(data, indent=2, ensure_ascii=False)
        except Exception:
            pass
        return str(data)
