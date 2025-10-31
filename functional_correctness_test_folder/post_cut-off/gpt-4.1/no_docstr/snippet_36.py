
from typing import List, Optional
from datetime import datetime
from rich.text import Text
from rich.panel import Panel
from rich.console import RenderableType


class LoadingScreenComponent:

    def __init__(self) -> None:
        pass

    def create_loading_screen(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw', custom_message: Optional[str] = None) -> List[str]:
        lines = []
        if custom_message:
            lines.append(custom_message)
        else:
            lines.append("Loading, please wait...")
        lines.append(f"Plan: {plan.capitalize()}")
        try:
            import pytz
            tz = pytz.timezone(timezone)
            now = datetime.now(tz)
            time_str = now.strftime('%Y-%m-%d %H:%M:%S')
        except Exception:
            time_str = "Unknown time"
        lines.append(f"Timezone: {timezone} | Time: {time_str}")
        return lines

    def create_loading_screen_renderable(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw', custom_message: Optional[str] = None) -> RenderableType:
        lines = self.create_loading_screen(plan, timezone, custom_message)
        text = Text("\n".join(lines))
        panel = Panel(text, title="Loading", border_style="blue")
        return panel
