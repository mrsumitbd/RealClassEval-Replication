
from typing import List, Optional
from datetime import datetime
import pytz
from rich.console import RenderableType
from rich.panel import Panel
from rich.text import Text
from rich.spinner import Spinner
from rich.align import Align


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
        current_time = datetime.now(tz).strftime('%H:%M:%S')
        lines = [
            f"Loading {plan.upper()} plan...",
            f"Current time: {current_time} ({timezone})",
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
        text = Text("\n".join(lines), style="bold cyan")
        spinner = Spinner('dots', style="yellow")
        content = Align.center(Text.assemble(spinner, "  ", text))
        return Panel(content, title="Loading", border_style="blue")
