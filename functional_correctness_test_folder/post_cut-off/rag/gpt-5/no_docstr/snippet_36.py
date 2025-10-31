from datetime import datetime, timezone as _timezone
from typing import List, Optional

try:
    from zoneinfo import ZoneInfo
except Exception:  # pragma: no cover
    ZoneInfo = None  # type: ignore[misc,assignment]

from rich.console import Group, RenderableType
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.spinner import Spinner


class LoadingScreenComponent:
    '''Loading screen component for displaying loading states.'''

    def __init__(self) -> None:
        '''Initialize loading screen component.'''
        self._plan_tips = {
            'pro': 'Pro tip: Enable caching and parallelism to speed up builds.',
            'basic': 'Tip: Upgrade to Pro for faster builds and advanced features.',
            'community': 'Tip: Join the community forum to get help and share feedback.',
            'enterprise': 'Enterprise: SSO, RBAC, and audit logs available.',
        }
        self._default_tip = 'Tip: Keep this window open while we prepare your workspace.'

    def create_loading_screen(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw', custom_message: Optional[str] = None) -> List[str]:
        '''Create loading screen content.
        Args:
            plan: Current plan name
            timezone: Display timezone
        Returns:
            List of loading screen lines
        '''
        tzinfo = None
        tz_label = timezone
        if ZoneInfo is not None:
            try:
                tzinfo = ZoneInfo(timezone)
            except Exception:
                tzinfo = _timezone.utc
                tz_label = 'UTC'
        else:
            tzinfo = _timezone.utc
            tz_label = 'UTC'

        now = datetime.now(tzinfo)
        time_str = now.strftime('%Y-%m-%d %H:%M:%S %Z')

        tip = self._plan_tips.get(plan.lower(), self._default_tip)

        lines: List[str] = []
        lines.append('Loading, please wait...')
        if custom_message:
            lines.append(custom_message)
        lines.append(f'Plan: {plan}')
        lines.append(f'Time: {time_str}')
        lines.append(f'Timezone: {tz_label}')
        lines.append('This may take a few moments...')
        lines.append(tip)
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

        header = Text('Preparing your environment', style='bold cyan')
        spinner = Spinner('dots', text=' Loading…', style='cyan')

        body = Group(
            header,
            Text(),
            *(Text(line) for line in lines),
        )

        content = Group(spinner, Text(), body)
        return Panel(
            Align.center(content, vertical='middle'),
            title='Please wait',
            border_style='cyan',
            padding=(1, 2),
        )
