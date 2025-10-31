
from typing import Any
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from google.protobuf.json_format import MessageToDict


class EventRenderer:
    """Stateful renderer that groups function calls with their responses."""

    def __init__(self) -> None:
        """Initialize the event renderer."""
        self._pending_function_call = None

    def render_event(self, obj: 'Event', console: 'Console') -> None:
        """Render the provided google.adk.events.Event to rich.console."""
        event_dict = MessageToDict(obj)
        if 'functionCall' in event_dict:
            self._flush_pending_function_call(console)
            self._pending_function_call = event_dict['functionCall']
        elif 'response' in event_dict and self._pending_function_call is not None:
            self._render_function_call_group(
                self._pending_function_call, event_dict['response'], console)
            self._pending_function_call = None
        else:
            self._flush_pending_function_call(console)
            # Render other event types (e.g., log messages) directly
            console.print(Panel(Text(str(event_dict))))

    def _flush_pending_function_call(self, console: 'Console') -> None:
        """Render any pending function call that hasn't been paired with a response."""
        if self._pending_function_call is not None:
            self._render_function_call_group(
                self._pending_function_call, {}, console)
            self._pending_function_call = None

    def _render_function_call_group(self, function_call: dict[str, Any], response: dict[str, Any], console: 'Console') -> None:
        """Render function call and response together in a grouped panel."""
        function_call_text = Text(str(function_call))
        response_text = Text(str(response))
        group_text = Text("\n").join([function_call_text, response_text])
        console.print(Panel(group_text))
