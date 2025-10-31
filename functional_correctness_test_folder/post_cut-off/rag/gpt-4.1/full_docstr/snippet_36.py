
from typing import List, Optional
from datetime import datetime
from rich.text import Text
from rich.panel import Panel
from rich.align import Align
from rich.console import RenderableType


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
        now = None
        try:
            import pytz
            tz = pytz.timezone(timezone)
            now = datetime.now(tz)
        except Exception:
            now = datetime.now()
        time_str = now.strftime('%Y-%m-%d %H:%M:%S')
        lines.append("🔄 Loading, please wait...")
        if custom_message:
            lines.append(custom_message)
        lines.append(f"Plan: [bold]{plan}[/bold]")
        lines.append(f"Time: [bold]{time_str}[/bold] ({timezone})")
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
            text.append(line)
            text.append('\n')
        panel = Panel(
            Align.center(text, vertical="middle"),
            title="Loading",
            border_style="cyan",
            padding=(1, 4)
        )
        return panel
