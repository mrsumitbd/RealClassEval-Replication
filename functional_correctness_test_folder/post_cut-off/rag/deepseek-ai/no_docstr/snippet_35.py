
from typing import List
import datetime
import pytz


class ErrorDisplayComponent:
    '''Error display component for handling error states.'''

    def __init__(self) -> None:
        '''Initialize error display component.'''
        pass

    def format_error_screen(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> List[str]:
        '''Format error screen for failed data fetch.
        Args:
            plan: Current plan name
            timezone: Display timezone
        Returns:
            List of formatted error screen lines
        '''
        tz = pytz.timezone(timezone)
        now = datetime.datetime.now(tz)
        timestamp = now.strftime('%Y-%m-%d %H:%M:%S %Z')

        error_lines = [
            "╔════════════════════════════════════════════╗",
            "║               ERROR REPORT                 ║",
            "╠════════════════════════════════════════════╣",
            f"║ Plan: {plan.ljust(36)} ║",
            f"║ Timestamp: {timestamp.ljust(27)} ║",
            "║                                            ║",
            "║  Failed to fetch data. Please check:       ║",
            "║  1. Your internet connection               ║",
            "║  2. API service status                     ║",
            "║  3. Your authentication credentials        ║",
            "║                                            ║",
            "║  Try refreshing or contact support if the  ║",
            "║  problem persists.                         ║",
            "╚════════════════════════════════════════════╝"
        ]

        return error_lines
