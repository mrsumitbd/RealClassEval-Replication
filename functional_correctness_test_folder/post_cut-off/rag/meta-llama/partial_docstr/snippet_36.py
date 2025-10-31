
from typing import List, Optional
from rich.console import RenderableType
from rich.panel import Panel
from rich.text import Text
from datetime import datetime
import pytz


class LoadingScreenComponent:
    """Loading screen component for displaying loading states."""

    def __init__(self) -> None:
        """Initialize loading screen component."""
        pass

    def create_loading_screen(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw', custom_message: Optional[str] = None) -> List[str]:
        """Create loading screen content.

        Args:
            plan: Current plan name
            timezone: Display timezone
        Returns:
            List of loading screen lines
        """
        lines = []
        current_time = datetime.now(pytz.timezone(
            timezone)).strftime('%Y-%m-%d %H:%M:%S %Z%z')
        lines.append(f'Current Time: {current_time}')
        lines.append(f'Plan: {plan}')
        if custom_message:
            lines.append(custom_message)
        lines.append('Loading...')
        return lines

    def create_loading_screen_renderable(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw', custom_message: Optional[str] = None) -> RenderableType:
        """Create Rich renderable for loading screen.

        Args:
            plan: Current plan name
            timezone: Display timezone
        Returns:
            Rich renderable for loading screen
        """
        lines = self.create_loading_screen(plan, timezone, custom_message)
        text = Text('\n'.join(lines))
        return Panel(text, title='Loading', border_style='red')
