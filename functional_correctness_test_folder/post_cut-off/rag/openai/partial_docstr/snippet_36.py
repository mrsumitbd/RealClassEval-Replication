
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

import pytz
from rich.console import RenderableType
from rich.panel import Panel
from rich.text import Text


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
        # Resolve timezone, fallback to UTC if invalid
        try:
            tz = pytz.timezone(timezone)
        except Exception:
            tz = pytz.utc
            timezone = "UTC"

        now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S %Z")

        lines: List[str] = [
            "Loading...",
            f"Plan: {plan}",
            f"Timezone: {timezone}",
            f"Time: {now}",
        ]

        if custom_message:
            lines.append(custom_message)

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
        # Build a styled Text object
        text = Text()
        for line in lines:
            text.append(line + "\n", style="bold cyan")
        # Wrap in a Panel for a nicer look
        panel = Panel(
            text,
            title="Loading",
            border_style="bright_blue",
            padding=(1, 2),
            expand=False,
        )
        return panel
