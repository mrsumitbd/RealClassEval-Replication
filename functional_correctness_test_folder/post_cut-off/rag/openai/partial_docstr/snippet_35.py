
from typing import List
from datetime import datetime
import pytz


class ErrorDisplayComponent:
    '''Error display component for handling error states.'''

    def __init__(self) -> None:
        '''Initialize error display component.'''
        # No internal state required for this simple component
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
            tz = pytz.timezone(timezone)
            now = datetime.now(tz)
            time_str = now.strftime('%Y-%m-%d %H:%M:%S %Z')
        except Exception:
            # Fallback to UTC if timezone is invalid
            now = datetime.utcnow()
            time_str = now.strftime('%Y-%m-%d %H:%M:%S UTC')

        # Build the error screen lines
        lines = [
            "========================================",
            "          ERROR: Data Fetch Failed       ",
            "========================================",
            f"Plan: {plan}",
            f"Time: {time_str}",
            "",
            "Possible causes:",
            "- Network connectivity issues",
            "- API rate limits exceeded",
            "- Server maintenance",
            "",
            "Suggested actions:",
            "- Check your internet connection",
            "- Retry after a few minutes",
            "- Contact support if the issue persists",
            "",
            "========================================",
        ]
        return lines
