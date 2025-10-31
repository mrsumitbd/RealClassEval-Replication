
from typing import List, Optional
from rich.console import RenderableType
from rich.panel import Panel
from rich.text import Text
from datetime import datetime
import pytz


class LoadingScreenComponent:
    '''Loading screen component for displaying loading states.'''

    def __init__(self) -> None:
        '''Initialize loading screen component.'''
        self.current_time = datetime.now(pytz.timezone('Europe/Warsaw'))

    def create_loading_screen(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw', custom_message: Optional[str] = None) -> List[str]:
        '''Create loading screen content.
        Args:
            plan: Current plan name
            timezone: Display timezone
        Returns:
            List of loading screen lines
        '''
        self.current_time = datetime.now(pytz.timezone(timezone))
        lines = [
            f"Current Plan: {plan}",
            f"Current Time: {self.current_time.strftime('%Y-%m-%d %H:%M:%S')}",
            "Loading... Please wait"
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
        text = Text("\n".join(lines), style="bold green")
        return Panel(text, title="Loading", border_style="blue", expand=False)
