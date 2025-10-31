
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from rich.console import RenderableType
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich import box
import pytz


class LoadingScreenComponent:
    """Loading screen component for displaying loading states."""

    def __init__(self) -> None:
        """Initialize loading screen component."""
        # No state needed for this simple component
        pass

    def create_loading_screen(
        self,
        plan: str = "pro",
        timezone: str = "Europe/Warsaw",
        custom_message: Optional[str] = None,
    ) -> List[str]:
        """Create loading screen content.

        Args:
            plan: Current plan name
            timezone: Display timezone
            custom_message: Optional custom message to display

        Returns:
            List of loading screen lines
        """
        # Current time in the requested timezone
        try:
            tz = pytz.timezone(timezone)
            now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S %Z")
        except Exception:
            now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

        lines = [
            f"[bold cyan]Loading...[/bold cyan]",
            f"[green]Plan:[/green] {plan}",
            f"[yellow]Timezone:[/yellow] {timezone}",
            f"[magenta]Current time:[/magenta] {now}",
        ]

        if custom_message:
            lines.append(f"[white]{custom_message}[/white]")

        return lines

    def create_loading_screen_renderable(
        self,
        plan: str = "pro",
        timezone: str = "Europe/Warsaw",
        custom_message: Optional[str] = None,
    ) -> RenderableType:
        """Create Rich renderable for loading screen.

        Args:
            plan: Current plan name
            timezone: Display timezone
            custom_message: Optional custom message to display

        Returns:
            Rich renderable for loading screen
        """
        lines = self.create_loading_screen(plan, timezone, custom_message)
        text = Text("\n".join(lines), justify="center")
        panel = Panel(
            Align.center(text),
            title="",
            border_style="bright_blue",
            box=box.ROUNDED,
            padding=(1, 2),
        )
        return panel
