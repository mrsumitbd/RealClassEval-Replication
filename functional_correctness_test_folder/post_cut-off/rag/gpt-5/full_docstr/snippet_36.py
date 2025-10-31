from typing import List, Optional
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from rich.console import RenderableType, Group
from rich.text import Text
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich.spinner import Spinner
from rich.rule import Rule
from rich import box
import random


class LoadingScreenComponent:
    '''Loading screen component for displaying loading states.'''

    def __init__(self) -> None:
        '''Initialize loading screen component.'''
        self._tips: List[str] = [
            'Tip: Press Ctrl+C to cancel.',
            'Tip: You can change settings later from the preferences menu.',
            'Tip: Use a faster plan for larger workloads.',
            'Tip: Logs are written to the .logs directory.',
            'Tip: Need help? Check the documentation or run with --help.',
        ]
        self._plan_styles = {
            'free': 'green',
            'basic': 'cyan',
            'pro': 'magenta',
            'team': 'yellow',
            'enterprise': 'bright_blue',
        }

    def create_loading_screen(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw', custom_message: Optional[str] = None) -> List[str]:
        '''Create loading screen content.
        Args:
            plan: Current plan name
            timezone: Display timezone
        Returns:
            List of loading screen lines
        '''
        tz_display = timezone
        try:
            tzinfo = ZoneInfo(timezone)
        except ZoneInfoNotFoundError:
            tzinfo = ZoneInfo('UTC')
            tz_display = 'UTC'
        now = datetime.now(tzinfo)

        plan_disp = (plan or '').strip() or 'unknown'
        plan_disp_upper = plan_disp.upper()

        lines: List[str] = []
        lines.append('Preparing your workspace...')
        lines.append(f'Plan: {plan_disp_upper}')
        lines.append(
            f'Time: {now.strftime("%Y-%m-%d %H:%M:%S")} ({tz_display})')
        if custom_message:
            lines.append(custom_message)
        else:
            lines.append('This may take a few moments.')
        lines.append(random.choice(self._tips))
        return lines

    def create_loading_screen_renderable(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw', custom_message: Optional[str] = None) -> RenderableType:
        '''Create Rich renderable for loading screen.
        Args:
            plan: Current plan name
            timezone: Display timezone
        Returns:
            Rich renderable for loading screen
        '''
        tz_display = timezone
        try:
            tzinfo = ZoneInfo(timezone)
        except ZoneInfoNotFoundError:
            tzinfo = ZoneInfo('UTC')
            tz_display = 'UTC'
        now = datetime.now(tzinfo)

        lines = self.create_loading_screen(
            plan=plan, timezone=timezone, custom_message=custom_message)

        plan_clean = (plan or '').strip().lower() or 'unknown'
        plan_style = self._plan_styles.get(plan_clean, 'white')

        header = Text('Loading', style='bold white')
        subheader = Text(
            'Please wait while we get things ready...', style='dim')

        spinner = Spinner('dots', text=Text('Initializing...', style='italic'))

        info = Table.grid(padding=(0, 1))
        info.add_column(justify='right', style='bold dim')
        info.add_column()
        info.add_row('Plan', Text(plan_clean.upper(),
                     style=f'bold {plan_style}'))
        info.add_row(
            'Time', f'{now.strftime("%Y-%m-%d %H:%M:%S")} ({tz_display})')

        details = Table.grid(expand=True)
        details.add_column()
        for line in lines:
            details.add_row(Text(line))

        content = Group(
            Align.center(header),
            Align.center(subheader),
            Rule(style='dim'),
            Align.center(spinner),
            Align.center(info),
            Rule(style='dim'),
            details,
        )

        panel = Panel(
            content,
            title='Setup',
            title_align='left',
            border_style='dim',
            box=box.ROUNDED,
            padding=(1, 2),
        )
        return panel
