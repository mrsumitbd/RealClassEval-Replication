
from typing import List, Optional
from typing_extensions import RenderableType
from datetime import datetime
import pytz


class LoadingScreenComponent:

    def __init__(self) -> None:
        pass

    def create_loading_screen(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw', custom_message: Optional[str] = None) -> List[str]:
        lines = []
        tz = pytz.timezone(timezone)
        current_time = datetime.now(tz).strftime("%H:%M:%S")

        lines.append(f"Loading Screen - {plan.upper()} Plan")
        lines.append(f"Current Time ({timezone}): {current_time}")

        if custom_message:
            lines.append(f"Message: {custom_message}")
        else:
            lines.append("Loading... Please wait.")

        return lines

    def create_loading_screen_renderable(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw', custom_message: Optional[str] = None) -> RenderableType:
        lines = self.create_loading_screen(plan, timezone, custom_message)
        return "\n".join(lines)
