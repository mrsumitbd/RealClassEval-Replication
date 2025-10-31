
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
        current_time = datetime.datetime.now(pytz.timezone(timezone))
        formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S %Z')

        error_lines = [
            "╔══════════════════════════════════════════════════╗",
            "║               DATA FETCH FAILED                  ║",
            "╠══════════════════════════════════════════════════╣",
            f"║ Plan: {plan.ljust(42)} ║",
            f"║ Time: {formatted_time.ljust(42)} ║",
            "║                                                  ║",
            "║  Please check your network connection and        ║",
            "║  try again later. If the problem persists,       ║",
            "║  contact support.                                ║",
            "╚══════════════════════════════════════════════════╝"
        ]

        return error_lines
