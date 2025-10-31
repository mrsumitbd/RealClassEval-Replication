from claude_monitor.ui.layouts import HeaderManager
from typing import Any, Dict, List, Optional
from rich.console import Console, RenderableType

class LoadingScreenComponent:
    """Loading screen component for displaying loading states."""

    def __init__(self) -> None:
        """Initialize loading screen component."""

    def create_loading_screen(self, plan: str='pro', timezone: str='Europe/Warsaw', custom_message: Optional[str]=None) -> List[str]:
        """Create loading screen content.

        Args:
            plan: Current plan name
            timezone: Display timezone

        Returns:
            List of loading screen lines
        """
        screen_buffer = []
        header_manager = HeaderManager()
        screen_buffer.extend(header_manager.create_header(plan, timezone))
        screen_buffer.append('')
        screen_buffer.append('[info]⏳ Loading...[/]')
        screen_buffer.append('')
        if custom_message:
            screen_buffer.append(f'[warning]{custom_message}[/]')
        else:
            screen_buffer.append('[warning]Fetching Claude usage data...[/]')
        screen_buffer.append('')
        if plan == 'custom' and (not custom_message):
            screen_buffer.append('[info]Calculating your P90 session limits from usage history...[/]')
            screen_buffer.append('')
        screen_buffer.append('[dim]This may take a few seconds[/]')
        return screen_buffer

    def create_loading_screen_renderable(self, plan: str='pro', timezone: str='Europe/Warsaw', custom_message: Optional[str]=None) -> RenderableType:
        """Create Rich renderable for loading screen.

        Args:
            plan: Current plan name
            timezone: Display timezone

        Returns:
            Rich renderable for loading screen
        """
        screen_buffer = self.create_loading_screen(plan, timezone, custom_message)
        from claude_monitor.ui.display_controller import ScreenBufferManager
        buffer_manager = ScreenBufferManager()
        return buffer_manager.create_screen_renderable(screen_buffer)