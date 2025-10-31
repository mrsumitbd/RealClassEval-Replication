
from typing import List, Optional
from rich.console import RenderableType
from rich.panel import Panel
from rich.text import Text
from rich import box
from datetime import datetime
import pytz


class LoadingScreenComponent:
    '''Loading screen component for displaying loading states.'''

    def __init__(self) -> None:
        '''Initialize loading screen component.'''
        self.loading_messages = [
            "Initializing components...",
            "Loading configuration...",
            "Preparing environment...",
            "Setting up resources...",
            "Finalizing setup..."
        ]

    def create_loading_screen(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw', custom_message: Optional[str] = None) -> List[str]:
        '''Create loading screen content.
        Args:
            plan: Current plan name
            timezone: Display timezone
        Returns:
            List of loading screen lines
        '''
        current_time = datetime.now(pytz.timezone(
            timezone)).strftime('%Y-%m-%d %H:%M:%S %Z')
        lines = [
            f"Current Plan: {plan}",
            f"Timezone: {timezone}",
            f"Current Time: {current_time}",
            "",
            "Loading...",
            ""
        ]

        if custom_message:
            lines.append(f"Status: {custom_message}")
        else:
            lines.extend(self.loading_messages)

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
        return Panel(
            text,
            title="Loading...",
            border_style="blue",
            box=box.ROUNDED,
            padding=(1, 2)
        )
