
from typing import Optional, List
from rich.text import Text
from rich.console import RenderableType
from datetime import datetime
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
        tz = pytz.timezone(timezone)
        current_time = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S %Z')
        lines = [
            "Loading...",
            f"Plan: {plan}",
            f"Timezone: {current_time}",
        ]
        if custom_message:
            lines.append(custom_message)
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
        renderable = Text("\n".join(lines), style="bold green")
        return renderable
