
from typing import Any, Dict, Optional
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.syntax import Syntax


class EventRenderer:
    '''Stateful renderer that groups function calls with their responses.'''

    def __init__(self) -> None:
        '''Initialize the event renderer.'''
        self._pending_function_call: Optional['FunctionCall'] = None
        self._pending_response: Optional[Dict[str, Any]] = None

    def render_event(self, obj: 'Event', console: 'Console') -> None:
        '''Render an event, handling function calls and responses.'''
        if hasattr(obj, 'function_call'):
            self._pending_function_call = obj.function_call
        elif hasattr(obj, 'content') and self._pending_function_call:
            self._pending_response = {'content': obj.content}
            self._flush_pending_function_call(console)
        elif hasattr(obj, 'content'):
            console.print(obj.content)

    def _flush_pending_function_call(self, console: 'Console') -> None:
        '''Render pending function call and response, then clear them.'''
        if self._pending_function_call and self._pending_response:
            self._render_function_call_group(
                self._pending_function_call, self._pending_response, console)
            self._pending_function_call = None
            self._pending_response = None

    def _render_function_call_group(self, function_call: 'FunctionCall', response: Dict[str, Any], console: 'Console') -> None:
        '''Render function call and response together in a grouped panel.'''
        function_text = Text(
            f"Function: {function_call.name}\nArguments: {function_call.arguments}", style="bold blue")
        response_text = Text(
            f"Response: {response.get('content', '')}", style="green")
        panel = Panel.fit(
            Text.assemble(function_text, "\n", response_text),
            title="Function Call",
            border_style="yellow"
        )
        console.print(panel)
