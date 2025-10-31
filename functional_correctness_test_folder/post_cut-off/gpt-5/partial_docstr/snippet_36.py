from typing import Optional, List
from datetime import datetime
try:
    from zoneinfo import ZoneInfo
except Exception:
    ZoneInfo = None  # type: ignore

from rich.console import RenderableType
from rich.text import Text
from rich.panel import Panel


class LoadingScreenComponent:

    def __init__(self) -> None:
        '''Initialize loading screen component.'''
        self.default_title = "Loading"
        self.default_tip = "Tip: Press Ctrl+C to cancel."
        self.default_message = "Preparing your workspace…"
        self._time_format = "%Y-%m-%d %H:%M:%S %Z"

    def _safe_zoneinfo(self, tz_name: str):
        if ZoneInfo is None:
            return None
        try:
            return ZoneInfo(tz_name)
        except Exception:
            try:
                return ZoneInfo("UTC")
            except Exception:
                return None

    def _current_time_str(self, timezone: str) -> str:
        tz = self._safe_zoneinfo(timezone)
        now = datetime.now(tz) if tz else datetime.utcnow()
        return now.strftime(self._time_format)

    def create_loading_screen(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw', custom_message: Optional[str] = None) -> List[str]:
        '''Create loading screen content.
        Args:
            plan: Current plan name
            timezone: Display timezone
        Returns:
            List of loading screen lines
        '''
        message = custom_message if custom_message else self.default_message
        plan_display = (plan or "").strip() or "unknown"
        time_display = self._current_time_str(timezone)
        lines = [
            f"{self.default_title}…",
            message,
            f"Plan: {plan_display}",
            f"Time: {time_display}",
            self.default_tip,
        ]
        return lines

    def create_loading_screen_renderable(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw', custom_message: Optional[str] = None) -> RenderableType:
        '''Create Rich renderable for loading screen.
        Args:
            plan: Current plan name
            timezone: Display timezone
        Returns:
            Rich renderable for loading screen
        '''
        lines = self.create_loading_screen(
            plan=plan, timezone=timezone, custom_message=custom_message)
        text = Text("\n".join(lines))
        return Panel(
            text,
            title="Please wait",
            border_style="cyan",
            padding=(1, 2),
        )
