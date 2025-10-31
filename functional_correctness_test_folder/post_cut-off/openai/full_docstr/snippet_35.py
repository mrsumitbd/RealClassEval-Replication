
from typing import List
import datetime
import pytz


class ErrorDisplayComponent:
    '''Error display component for handling error states.'''

    def __init__(self) -> None:
        '''Initialize error display component.'''
        # No state needed for now, but placeholder for future extensions
        pass

    def format_error_screen(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> List[str]:
        '''Format error screen for failed data fetch.
        Args:
            plan: Current plan name
            timezone: Display timezone
        Returns:
            List of formatted error screen lines
        '''
        # Get current time in the specified timezone
        try:
            tz = pytz.timezone(timezone)
            now = datetime.datetime.now(tz)
            time_str = now.strftime('%Y-%m-%d %H:%M:%S %Z')
        except Exception:
            time_str = f'Unknown timezone: {timezone}'

        # Build the error screen lines
        lines = [
            "========================================",
            "            ERROR: FETCH FAILED          ",
            "========================================",
            f"Time: {time_str}",
            f"Plan: {plan}",
            "",
            "Please check your network connection and try again.",
            "If the problem persists, contact support.",
            "========================================",
        ]
        return lines
