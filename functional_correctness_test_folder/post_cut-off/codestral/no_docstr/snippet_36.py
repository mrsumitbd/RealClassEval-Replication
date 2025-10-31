
from typing import List, Optional
from rich.console import RenderableType
from rich.panel import Panel
from rich.text import Text


class LoadingScreenComponent:

    def __init__(self) -> None:
        pass

    def create_loading_screen(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw', custom_message: Optional[str] = None) -> List[str]:
        loading_screen = [
            "Loading...",
            f"Plan: {plan}",
            f"Timezone: {timezone}"
        ]
        if custom_message:
            loading_screen.append(f"Message: {custom_message}")
        return loading_screen

    def create_loading_screen_renderable(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw', custom_message: Optional[str] = None) -> RenderableType:
        loading_text = Text("Loading...", style="bold")
        plan_text = Text(f"Plan: {plan}", style="italic")
        timezone_text = Text(f"Timezone: {timezone}", style="italic")
        renderables = [loading_text, plan_text, timezone_text]
        if custom_message:
            message_text = Text(f"Message: {custom_message}", style="italic")
            renderables.append(message_text)
        return Panel("\n".join(renderable.plain for renderable in renderables), title="Loading Screen", border_style="blue")
