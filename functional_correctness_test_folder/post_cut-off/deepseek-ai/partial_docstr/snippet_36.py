
from typing import List, Optional
from datetime import datetime
import pytz
from rich.console import RenderableType
from rich.panel import Panel
from rich.text import Text
from rich.spinner import Spinner
from rich.align import Align


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
        tz = pytz.timezone(timezone)
        current_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        lines = [
            f"Loading... (Plan: {plan})",
            f"Current time: {current_time} ({timezone})",
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
        tz = pytz.timezone(timezone)
        current_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        text = Text()
        text.append("Loading... ", style="bold blue")
        text.append(f"(Plan: {plan})\n", style="bold green")
        text.append(
            f"Current time: {current_time} ({timezone})\n", style="italic")
        if custom_message:
            text.append(f"Message: {custom_message}", style="yellow")
        spinner = Spinner('dots', style="magenta")
        content = Align.center(spinner)
        panel = Panel(
            content,
            title="[b]System Status[/b]",
            subtitle=text,
            border_style="blue",
            padding=(1, 2),
        )
        return panel
