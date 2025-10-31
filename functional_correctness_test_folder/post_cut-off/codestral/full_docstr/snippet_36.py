
from typing import List, Optional
from rich.console import RenderableType
from rich.panel import Panel
from rich.text import Text


class LoadingScreenComponent:
    '''Loading screen component for displaying loading states.'''

    def __init__(self) -> None:
        '''Initialize loading screen component.'''
        pass

    def create_loading_screen(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw', custom_message: Optional[str] = None) -> List[str]:
        '''Create loading screen content.
        Args:
            plan: Current plan name
            timezone: Display timezone
        Returns:
            List of loading screen lines
        '''
        lines = [
            "Loading...",
            f"Plan: {plan}",
            f"Timezone: {timezone}"
        ]
        if custom_message:
            lines.append(f"Message: {custom_message}")
        return lines

    def create_loading_screen_renderable(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw', custom_message: Optional[str] = None) -> RenderableType:
        '''Create Rich renderable for loading screen.
        Args:
            plan: Current plan name
            timezone: Display timezone
        Returns:
            Rich renderable for loading screen
        '''
        lines = self.create_loading_screen(plan, timezone, custom_message)
        text = Text("\n".join(lines))
        return Panel(text, title="Loading", border_style="blue")
