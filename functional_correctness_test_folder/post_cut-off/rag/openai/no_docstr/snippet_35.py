
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import List


class ErrorDisplayComponent:
    '''Error display component for handling error states.'''

    def __init__(self) -> None:
        '''Initialize error display component.'''
        # No state needed for now
        pass

    def format_error_screen(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> List[str]:
        '''Format error screen for failed data fetch.
        Args:
            plan: Current plan name
            timezone: Display timezone
        Returns:
            List of formatted error screen lines
        '''
        # Get current time in the requested timezone
        try:
            tz = ZoneInfo(timezone)
        except Exception:
            tz = ZoneInfo('UTC')
        now = datetime.now(tz)
        timestamp = now.strftime('%Y-%m-%d %H:%M:%S %Z')

        # Build the error screen lines
        lines = [
            "========================================",
            "            ERROR: DATA FETCH FAILED    ",
            "========================================",
            f"Timestamp: {timestamp}",
            f"Plan: {plan}",
            f"Timezone: {timezone}",
            "",
            "Unable to retrieve the requested data.",
            "Please check your network connection and try again.",
            "",
            "If the issue persists, contact support at support@example.com.",
            "",
            "========================================",
        ]
        return lines
