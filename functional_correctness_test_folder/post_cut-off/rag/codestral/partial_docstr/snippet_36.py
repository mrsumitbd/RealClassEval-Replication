
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
        self.default_messages = {
            'pro': "Loading your Pro plan dashboard...",
            'basic': "Loading your Basic plan dashboard...",
            'enterprise': "Loading your Enterprise plan dashboard..."
        }

    def create_loading_screen(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw', custom_message: Optional[str] = None) -> List[str]:
        '''Create loading screen content.
        Args:
            plan: Current plan name
            timezone: Display timezone
        Returns:
            List of loading screen lines
        '''
        now = datetime.now(pytz.timezone(timezone))
        formatted_time = now.strftime("%Y-%m-%d %H:%M:%S %Z")

        message = custom_message if custom_message else self.default_messages.get(
            plan.lower(), "Loading your dashboard...")

        return [
            f"Current Plan: {plan.capitalize()}",
            f"Time: {formatted_time}",
            message,
            "Please wait while we prepare your dashboard..."
        ]

    def create_loading_screen_renderable(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw', custom_message: Optional[str] = None) -> RenderableType:
        '''Create Rich renderable for loading screen.
        Args:
            plan: Current plan name
            timezone: Display timezone
        Returns:
            Rich renderable for loading screen
        '''
        lines = self.create_loading_screen(plan, timezone, custom_message)
        text = Text("\n".join(lines), justify="center")

        return Panel(
            text,
            title="Loading Dashboard",
            border_style="blue",
            padding=(1, 2),
            expand=False
        )
