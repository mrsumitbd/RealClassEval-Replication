
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from typing import Any


class Event:
    def __init__(self, type: str, data: dict):
        self.type = type
        self.data = data


class FunctionCall:
    def __init__(self, name: str, args: dict):
        self.name = name
        self.args = args


class EventRenderer:
    '''Stateful renderer that groups function calls with their responses.'''

    def __init__(self) -> None:
        '''Initialize the event renderer.'''
        self.pending_function_call = None

    def render_event(self, obj: 'Event', console: 'Console') -> None:
        '''Render the provided google.adk.events.Event to rich.console.'''
        if obj.type == 'function_call':
            self._flush_pending_function_call(console)
            self.pending_function_call = obj.data
        elif obj.type == 'function_response':
            if self.pending_function_call is not None:
                self._render_function_call_group(
                    self.pending_function_call, obj.data, console)
                self.pending_function_call = None
            else:
                console.print(
                    Panel(Text(f"Unexpected function response: {obj.data}"), title="Error"))
        else:
            self._flush_pending_function_call(console)
            console.print(
                Panel(Text(f"Event type: {obj.type}, Data: {obj.data}"), title=obj.type))

    def _flush_pending_function_call(self, console: 'Console') -> None:
        '''Render any pending function call that hasn't been paired with a response.'''
        if self.pending_function_call is not None:
            self._render_function_call_group(
                self.pending_function_call, None, console)
            self.pending_function_call = None

    def _render_function_call_group(self, function_call: 'FunctionCall', response: dict[str, Any], console: 'Console') -> None:
        '''Render function call and response together in a grouped panel.'''
        function_call_text = Text(
            f"Function Call: {function_call['name']}({function_call['args']})")
        if response is not None:
            response_text = Text(f"Response: {response}")
            console.print(Panel([function_call_text, Text(
                "\n"), response_text], title="Function Call and Response"))
        else:
            console.print(Panel(function_call_text,
                          title="Pending Function Call"))
