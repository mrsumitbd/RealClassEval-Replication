
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from typing import Any


class Event:
    def __init__(self, function_call=None, response=None):
        self.function_call = function_call
        self.response = response


class FunctionCall:
    def __init__(self, name, args, kwargs):
        self.name = name
        self.args = args
        self.kwargs = kwargs


class EventRenderer:
    '''Stateful renderer that groups function calls with their responses.'''

    def __init__(self) -> None:
        '''Initialize the event renderer.'''
        self.pending_function_call = None

    def render_event(self, obj: 'Event', console: 'Console') -> None:
        if obj.function_call is not None:
            if self.pending_function_call is not None:
                self._flush_pending_function_call(console)
            self.pending_function_call = obj.function_call
        elif obj.response is not None and self.pending_function_call is not None:
            self._render_function_call_group(
                self.pending_function_call, obj.response, console)
            self.pending_function_call = None

    def _flush_pending_function_call(self, console: 'Console') -> None:
        # Render the pending function call without a response
        self._render_function_call_group(
            self.pending_function_call, {}, console)
        self.pending_function_call = None

    def _render_function_call_group(self, function_call: 'FunctionCall', response: dict[str, Any], console: 'Console') -> None:
        '''Render function call and response together in a grouped panel.'''
        function_call_text = Text(f"Function Call: {function_call.name}\n")
        function_call_text.append(f"Args: {function_call.args}\n")
        function_call_text.append(f"Kwargs: {function_call.kwargs}\n")

        response_text = Text(f"Response: {response}\n")

        panel_text = Text.assemble(function_call_text, response_text)
        panel = Panel(panel_text, title="Event")
        console.print(panel)


# Example usage:
if __name__ == "__main__":
    console = Console()
    renderer = EventRenderer()

    function_call = FunctionCall(
        "example_function", [1, 2, 3], {"key": "value"})
    event1 = Event(function_call=function_call)
    renderer.render_event(event1, console)

    response = {"result": "success"}
    event2 = Event(response=response)
    renderer.render_event(event2, console)
