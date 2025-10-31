from typing import Any, Optional


class EventRenderer:
    '''Stateful renderer that groups function calls with their responses.'''

    def __init__(self) -> None:
        '''Initialize the event renderer.'''
        self._pending_function_call: Optional['FunctionCall'] = None
        self._pending_response: Optional[dict[str, Any]] = None

    def render_event(self, obj: 'Event', console: 'Console') -> None:
        '''Render the provided google.adk.events.Event to rich.console.'''
        if hasattr(obj, "function_call") and obj.function_call is not None:
            # If there is a pending function call, flush it before rendering the new one
            self._flush_pending_function_call(console)
            self._pending_function_call = obj.function_call
            self._pending_response = None
        elif hasattr(obj, "function_response") and obj.function_response is not None:
            if self._pending_function_call is not None:
                self._render_function_call_group(
                    self._pending_function_call, obj.function_response, console)
                self._pending_function_call = None
                self._pending_response = None
            else:
                # No pending function call, just print the response
                console.print(
                    "[bold yellow]Orphaned function response:[/bold yellow]")
                console.print(obj.function_response)
        else:
            # Not a function call or response, flush any pending call
            self._flush_pending_function_call(console)
            # Render the event directly
            console.print(obj)

    def _flush_pending_function_call(self, console: 'Console') -> None:
        '''Render any pending function call that hasn't been paired with a response.'''
        if self._pending_function_call is not None:
            panel = None
            try:
                from rich.panel import Panel
                from rich.pretty import Pretty
                panel = Panel(
                    Pretty(self._pending_function_call),
                    title="[bold blue]Function Call (no response)[/bold blue]",
                    border_style="blue"
                )
            except ImportError:
                panel = str(self._pending_function_call)
            if panel is not None:
                console.print(panel)
            self._pending_function_call = None
            self._pending_response = None

    def _render_function_call_group(self, function_call: 'FunctionCall', response: dict[str, Any], console: 'Console') -> None:
        '''Render function call and response together in a grouped panel.'''
        try:
            from rich.panel import Panel
            from rich.columns import Columns
            from rich.pretty import Pretty
            call_panel = Panel(
                Pretty(function_call),
                title="[bold blue]Function Call[/bold blue]",
                border_style="blue"
            )
            response_panel = Panel(
                Pretty(response),
                title="[bold green]Response[/bold green]",
                border_style="green"
            )
            group_panel = Panel(
                Columns([call_panel, response_panel]),
                title="[bold magenta]Function Call & Response[/bold magenta]",
                border_style="magenta"
            )
            console.print(group_panel)
        except ImportError:
            console.print("Function Call:", function_call)
            console.print("Response:", response)
