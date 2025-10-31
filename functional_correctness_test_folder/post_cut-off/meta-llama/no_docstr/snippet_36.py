
from typing import List, Optional
from rich.console import RenderableType
from rich.text import Text
from datetime import datetime
import pytz


class LoadingScreenComponent:

    def __init__(self) -> None:
        pass

    def create_loading_screen(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw', custom_message: Optional[str] = None) -> List[str]:
        renderable = self.create_loading_screen_renderable(
            plan, timezone, custom_message)
        return [str(renderable)]

    def create_loading_screen_renderable(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw', custom_message: Optional[str] = None) -> RenderableType:
        tz = pytz.timezone(timezone)
        current_time = datetime.now(tz).strftime("%H:%M:%S")

        text = Text(f"Loading {plan} plan...\n")
        text.append(f"Current Time ({timezone}): {current_time}\n")

        if custom_message:
            text.append(custom_message + "\n")

        return text
