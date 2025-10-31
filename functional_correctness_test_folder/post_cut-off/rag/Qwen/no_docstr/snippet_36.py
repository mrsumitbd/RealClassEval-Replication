
from typing import List, Optional
from rich.console import RenderableType
from rich.text import Text
from rich.panel import Panel
from rich.spinner import Spinner
from datetime import datetime
import pytz


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
        tz = pytz.timezone(timezone)
        current_time = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S %Z')
        lines = [
            f"Loading... Plan: {plan}",
            f"Timezone: {current_time}",
            f"Custom Message: {custom_message}" if custom_message else "Custom Message: None"
        ]
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
        current_time = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S %Z')
        message = f"Plan: {plan}\nTimezone: {current_time}"
        if custom_message:
            message += f"\nCustom Message: {custom_message}"
        else:
            message += "\nCustom Message: None"
        text = Text(message, style="bold white")
        panel = Panel(Spinner("dots", text=text, style="bold white"),
                      title="Loading", style="bold white on blue")
        return panel
