
from typing import List, Optional
from rich.text import Text
from rich.panel import Panel
from rich.align import Align
from rich.console import RenderableType
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
        lines = []
        lines.append("⏳ Loading, please wait...")
        if custom_message:
            lines.append(custom_message)
        now = None
        try:
            tz = pytz.timezone(timezone)
            now = datetime.now(tz)
            time_str = now.strftime('%Y-%m-%d %H:%M:%S')
        except Exception:
            time_str = "Unknown time"
        lines.append(f"Plan: {plan}")
        lines.append(f"Timezone: {timezone}")
        lines.append(f"Current time: {time_str}")
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
        text = Text()
        for line in lines:
            text.append(line + "\n")
        panel = Panel(
            Align.center(text, vertical="middle"),
            title="Loading",
            border_style="cyan"
        )
        return panel
