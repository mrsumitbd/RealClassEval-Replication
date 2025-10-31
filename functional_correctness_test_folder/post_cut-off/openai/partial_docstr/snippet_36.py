
from __future__ import annotations

from typing import List, Optional

from rich.console import RenderableType
from rich.panel import Panel
from rich.text import Text


class LoadingScreenComponent:
    """
    Component responsible for generating a loading screen.
    """

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
        """
        Create loading screen content.

        Args:
            plan: Current plan name.
            timezone: Display timezone.
            custom_message: Optional custom message to display.

        Returns:
            List of loading screen lines.
        """
        lines: List[str] = [
            f"[bold cyan]Loading...[/bold cyan]",
            f"Plan: [green]{plan}[/green]",
            f"Timezone: [yellow]{timezone}[/yellow]",
        ]

        if custom_message:
            lines.append(f"[italic]{custom_message}[/italic]")

        return lines

    def create_loading_screen_renderable(
        self,
        plan: str = "pro",
        timezone: str = "Europe/Warsaw",
        custom_message: Optional[str] = None,
    ) -> RenderableType:
        """
        Create Rich renderable for loading screen.

        Args:
            plan: Current plan name.
            timezone: Display timezone.
            custom_message: Optional custom message to display.

        Returns:
            Rich renderable for loading screen.
        """
        lines = self.create_loading_screen(plan, timezone, custom_message)
        # Join lines into a single Text object with newlines
        content = Text("\n".join(lines), justify="center")
        # Wrap the content in a Panel for a nicer appearance
        panel = Panel(
            content,
            title="Please Wait",
            border_style="bright_blue",
            padding=(1, 2),
            expand=False,
        )
        return panel
