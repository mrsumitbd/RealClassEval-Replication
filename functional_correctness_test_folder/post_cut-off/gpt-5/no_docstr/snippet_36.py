from typing import List, Optional
from datetime import datetime
from zoneinfo import ZoneInfo

from rich.console import RenderableType
from rich.text import Text
from rich.panel import Panel
from rich.align import Align
from rich import box


class LoadingScreenComponent:
    def __init__(self) -> None:
        self._plan_icons = {
            "free": "🟢",
            "pro": "🔵",
            "enterprise": "🟣",
        }
        self._plan_styles = {
            "free": "green",
            "pro": "cyan",
            "enterprise": "magenta",
        }

    def create_loading_screen(
        self,
        plan: str = "pro",
        timezone: str = "Europe/Warsaw",
        custom_message: Optional[str] = None,
    ) -> List[str]:
        plan_key = (plan or "").strip().lower() or "pro"
        plan_display = plan_key.title()
        icon = self._plan_icons.get(plan_key, "🔷")

        try:
            tz = ZoneInfo(timezone)
            tz_used = timezone
        except Exception:
            tz = ZoneInfo("UTC")
            tz_used = "UTC"

        now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S %Z")
        header = f"{icon} Loading ({plan_display} plan)"
        status = custom_message or "Preparing your workspace..."
        tz_line = f"Timezone: {tz_used} | Local time: {now}"
        note = "This may take a few seconds..."

        return [header, status, tz_line, note]

    def create_loading_screen_renderable(
        self,
        plan: str = "pro",
        timezone: str = "Europe/Warsaw",
        custom_message: Optional[str] = None,
    ) -> RenderableType:
        lines = self.create_loading_screen(
            plan=plan, timezone=timezone, custom_message=custom_message)

        plan_key = (plan or "").strip().lower() or "pro"
        plan_style = self._plan_styles.get(plan_key, "blue")

        text = Text()
        text.append(lines[0] + "\n", style=f"bold {plan_style}")
        text.append(lines[1] + "\n", style="white")
        text.append(lines[2] + "\n", style="dim")
        text.append(lines[3], style="italic dim")

        panel = Panel(
            Align.center(text, vertical="middle"),
            box=box.ROUNDED,
            border_style=plan_style,
            padding=(1, 2),
        )
        return panel
