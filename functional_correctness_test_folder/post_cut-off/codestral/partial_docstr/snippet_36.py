
from typing import List, Optional
from rich.console import RenderableType
from rich.panel import Panel
from rich.text import Text
import datetime
import pytz


class LoadingScreenComponent:

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
        lines = []
        lines.append("Loading...")
        lines.append(f"Plan: {plan}")
        tz = pytz.timezone(timezone)
        current_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        lines.append(f"Time: {current_time}")
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
        return Panel(text, title="Loading Screen", border_style="blue")
