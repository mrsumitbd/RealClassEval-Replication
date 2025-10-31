
from typing import List, Optional
from datetime import datetime
import pytz


class LoadingScreenComponent:

    def __init__(self) -> None:
        pass

    def create_loading_screen(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw', custom_message: Optional[str] = None) -> List[str]:
        tz = pytz.timezone(timezone)
        current_time = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S %Z%z')
        message = custom_message if custom_message else f"Loading {plan} plan at {current_time}"
        return [message]

    def create_loading_screen_renderable(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw', custom_message: Optional[str] = None) -> str:
        loading_screen = self.create_loading_screen(
            plan, timezone, custom_message)
        return "\n".join(loading_screen)
