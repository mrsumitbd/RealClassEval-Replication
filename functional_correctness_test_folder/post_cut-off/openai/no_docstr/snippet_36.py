
from __future__ import annotations

from typing import List, Optional

from rich.console import RenderableType
from rich.panel import Panel
from rich.text import Text


class LoadingScreenComponent:
    """
    A simple component that generates a loading screen representation.
    """

    def __init__(self) -> None:
        """
        Initialise the component. No state is required for this simple implementation.
        """
        pass

    def create_loading_screen(
        self,
        plan: str = "pro",
        timezone: str = "Europe/Warsaw",
        custom_message: Optional[str] = None,
    ) -> List[str]:
        """
        Create a textual representation of a loading screen.

        Parameters
        ----------
        plan : str, optional
            The subscription plan to display. Defaults to "pro".
        timezone : str, optional
            The timezone to display. Defaults to "Europe/Warsaw".
        custom_message : Optional[str], optional
            A custom message to display. If None, a default message is used.

        Returns
        -------
        List[str]
            A list of strings representing the loading screen lines.
        """
        lines: List[str] = []

        # Header
        lines.append("╔═══════════════════════════════════╗")
        lines.append("║          Loading...               ║")
        lines.append("╠═══════════════════════════════════╣")

        # Plan and timezone
        lines.append(f"║ Plan: {plan:<20} ║")
        lines.append(f"║ Timezone: {timezone:<15} ║")

        # Custom or default message
        message = custom_message or "Please wait while we prepare your environment."
        # Wrap the message to fit within the panel width (30 chars)
        wrapped = self._wrap_text(message, width=30)
        for line in wrapped:
            lines.append(f"║ {line:<30} ║")

        # Footer
        lines.append("╚═══════════════════════════════════╝")

        return lines

    def create_loading_screen_renderable(
        self,
        plan: str = "pro",
        timezone: str = "Europe/Warsaw",
        custom_message: Optional[str] = None,
    ) -> RenderableType:
        """
        Create a Rich renderable (Panel) that represents the loading screen.

        Parameters
        ----------
        plan : str, optional
            The subscription plan to display. Defaults to "pro".
        timezone : str, optional
            The timezone to display. Defaults to "Europe/Warsaw".
        custom_message : Optional[str], optional
            A custom message to display. If None, a default message is used.

        Returns
        -------
        RenderableType
            A Rich Panel that can be printed to the console.
        """
        # Build the content as a Text object
        content = Text()
        content.append("Loading...\n", style="bold cyan")
        content.append(f"Plan: {plan}\n", style="green")
        content.append(f"Timezone: {timezone}\n", style="green")
        message = custom_message or "Please wait while we prepare your environment."
        content.append(message, style="yellow")

        panel = Panel(
            content,
            title="Loading Screen",
            border_style="blue",
            padding=(1, 2),
        )
        return panel

    @staticmethod
    def _wrap_text(text: str, width: int) -> List[str]:
        """
        Simple word-wrapping helper.

        Parameters
        ----------
        text : str
            The text to wrap.
        width : int
            The maximum width of each line.

        Returns
        -------
        List[str]
            Wrapped lines.
        """
        words = text.split()
        lines: List[str] = []
        current: List[str] = []

        for word in words:
            if sum(len(w) for w in current) + len(current) + len(word) <= width:
                current.append(word)
            else:
                lines.append(" ".join(current))
                current = [word]
        if current:
            lines.append(" ".join(current))
        return lines
