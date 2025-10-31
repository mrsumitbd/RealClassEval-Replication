from __future__ import annotations

from typing import List, Optional
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from rich.console import RenderableType
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich import box


class LoadingScreenComponent:
    '''Loading screen component for displaying loading states.'''

    def __init__(self) -> None:
        '''Initialize loading screen component.'''
        self._app_name = "Loading"
        self._default_message = "Preparing your workspace..."
        self._plan_labels = {
            "free": "Free",
            "basic": "Basic",
            "pro": "Pro",
            "team": "Team",
            "enterprise": "Enterprise",
        }

    def _now_in_timezone(self, tz_name: str) -> datetime:
        try:
            tz = ZoneInfo(tz_name)
        except ZoneInfoNotFoundError:
            tz = ZoneInfo("UTC")
        return datetime.now(tz)

    def _format_time(self, dt: datetime) -> str:
        return dt.strftime("%Y-%m-%d %H:%M:%S %Z")

    def create_loading_screen(self, plan: str = "pro", timezone: str = "Europe/Warsaw", custom_message: Optional[str] = None) -> List[str]:
        '''Create loading screen content.
        Args:
            plan: Current plan name
            timezone: Display timezone
        Returns:
            List of loading screen lines
        '''
        dt = self._now_in_timezone(timezone)
        time_str = self._format_time(dt)

        plan_label = self._plan_labels.get(
            plan.lower(), plan.title() if plan else "Unknown")

        message = custom_message if (
            custom_message and custom_message.strip()) else self._default_message

        lines: List[str] = []
        lines.append(f"{self._app_name}")
        lines.append("")
        lines.append(message)
        lines.append("")
        lines.append(f"Plan: {plan_label}")
        lines.append(f"Time: {time_str}")
        return lines

    def create_loading_screen_renderable(self, plan: str = "pro", timezone: str = "Europe/Warsaw", custom_message: Optional[str] = None) -> RenderableType:
        '''Create Rich renderable for loading screen.
        Args:
            plan: Current plan name
            timezone: Display timezone
        Returns:
            Rich renderable for loading screen
        '''
        lines = self.create_loading_screen(
            plan=plan, timezone=timezone, custom_message=custom_message)

        table = Table.grid(padding=(0, 1))
        table.add_column(justify="left")
        for i, line in enumerate(lines):
            if i == 0:
                table.add_row(Text(line, style="bold cyan"))
            elif line.strip() == "":
                table.add_row(Text(""))
            elif line.startswith("Plan:"):
                table.add_row(Text(line, style="bold"))
            elif line.startswith("Time:"):
                table.add_row(Text(line, style="dim"))
            else:
                table.add_row(Text(line))

        return Panel(
            table,
            title="Please wait",
            title_align="left",
            border_style="cyan",
            box=box.ROUNDED,
            padding=(1, 2),
        )
