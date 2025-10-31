from __future__ import annotations

from typing import List, Optional
from datetime import datetime
try:
    from zoneinfo import ZoneInfo  # Python 3.9+
except Exception:  # pragma: no cover
    ZoneInfo = None  # type: ignore

from rich.console import RenderableType
from rich.panel import Panel
from rich.text import Text


class LoadingScreenComponent:
    '''Loading screen component for displaying loading states.'''

    def __init__(self) -> None:
        '''Initialize loading screen component.'''
        self._tips: List[str] = [
            'You can press Ctrl+C to cancel and try again later.',
            'Pro tip: keep your dependencies updated for best performance.',
            'Need help? Check the docs or contact support.',
            'Your settings are synced across devices on Pro plans.',
            'Customize your experience in Settings anytime.',
        ]

    def create_loading_screen(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw', custom_message: Optional[str] = None) -> List[str]:
        '''Create loading screen content.
        Args:
            plan: Current plan name
            timezone: Display timezone
        Returns:
            List of loading screen lines
        '''
        plan_disp = (plan or '').strip() or 'pro'
        message = custom_message or 'Setting things up for a smooth experience...'

        # Resolve current time in requested timezone
        try:
            if ZoneInfo is not None:
                tzinfo = ZoneInfo(timezone)
                now = datetime.now(tzinfo)
            else:
                raise Exception('ZoneInfo unavailable')  # fallback to UTC
            time_str = now.strftime('%Y-%m-%d %H:%M:%S')
            time_line = f'Time: {time_str} ({timezone})'
        except Exception:
            now = datetime.utcnow()
            time_str = now.strftime('%Y-%m-%d %H:%M:%S')
            time_line = f'Time: {time_str} (UTC)'

        # Deterministic tip selection based on minute to avoid randomness in tests
        tip_idx = now.minute % len(self._tips) if self._tips else 0
        tip = self._tips[tip_idx] if self._tips else ''

        lines: List[str] = [
            'Preparing your workspace...',
            message,
            f'Plan: {plan_disp.upper()}',
            time_line,
        ]
        if tip:
            lines.append(f'Tip: {tip}')
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
        body = Text()
        if lines:
            body.append(lines[0] + '\n', style='bold')
            for line in lines[1:]:
                body.append(line + '\n', style='dim')
        title = f'{(plan or "pro").upper()} PLAN'
        return Panel.fit(
            body,
            title=title,
            border_style='cyan',
            padding=(1, 2),
        )
