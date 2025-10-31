
from __future__ import annotations

from typing import List, Optional

from rich.align import Align
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

        Returns:
            List of loading screen lines
        """
        lines: List[str] = [
            "⏳ Loading...",
            f"Plan: {plan}",
            f"Timezone: {timezone}",
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

        Returns:
            Rich renderable for loading screen
        """
        lines = self.create_loading_screen(plan, timezone, custom_message)
        # Build a Text object with each line
        text = Text()
        for line in lines:
            text.append(line)
            text.append("\n")
        # Remove the trailing newline
        if text.plain.endswith("\n"):
            text.plain = text.plain.rstrip("\n")
        # Center the text inside a panel
        panel = Panel(
            Align.center(text, vertical="middle"),
            title="Loading",
            border_style="cyan",
            padding=(1, 2),
        )
        return panel
