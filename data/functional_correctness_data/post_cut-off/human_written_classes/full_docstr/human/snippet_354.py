from typing import TYPE_CHECKING, Any
from streetrace.ui.colors import Styles

class EventRenderer:
    """Stateful renderer that groups function calls with their responses."""

    def __init__(self) -> None:
        """Initialize the event renderer."""
        self.pending_function_call: tuple[str, FunctionCall] | None = None

    def render_event(self, obj: 'Event', console: 'Console') -> None:
        """Render the provided google.adk.events.Event to rich.console."""
        from rich.panel import Panel
        author = f'[bold]{obj.event.author}:[/bold]'
        if obj.event.is_final_response() and obj.event.actions and obj.event.actions.escalate:
            console.print(author, f"Agent escalated: {obj.event.error_message or 'No specific message.'}", style=Styles.RICH_ERROR)
        if obj.event.content and obj.event.content.parts:
            for part in obj.event.content.parts:
                if part.text:
                    self._flush_pending_function_call(console)
                    _display_assistant_text(part.text, obj.event.is_final_response(), console)
                if part.function_call:
                    self.pending_function_call = (author, part.function_call)
                if part.function_response and part.function_response.response:
                    if self.pending_function_call:
                        self._render_function_call_group(self.pending_function_call[1], part.function_response.response, console)
                        self.pending_function_call = None
                    else:
                        console.print(Panel(_format_function_response(part.function_response.response), title='Function Response', border_style='blue'))
        self._flush_pending_function_call(console)

    def _flush_pending_function_call(self, console: 'Console') -> None:
        """Render any pending function call that hasn't been paired with a response."""
        from rich.panel import Panel
        if self.pending_function_call:
            author, function_call = self.pending_function_call
            console.print(Panel(_format_function_call(function_call), title=f'{author} Function Call', border_style='yellow'))
            self.pending_function_call = None

    def _render_function_call_group(self, function_call: 'FunctionCall', response: dict[str, Any], console: 'Console') -> None:
        """Render function call and response together in a grouped panel."""
        from rich.panel import Panel
        call_content = _format_function_call(function_call)
        response_content = _format_function_response(response)
        from rich.console import Group
        combined_content = Group(call_content, '', response_content)
        console.print(Panel(combined_content, border_style='cyan'))