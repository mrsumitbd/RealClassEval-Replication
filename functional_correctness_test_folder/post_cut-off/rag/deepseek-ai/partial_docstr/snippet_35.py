
from typing import List
from datetime import datetime
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
        current_time = datetime.now(pytz.timezone(
            timezone)).strftime('%Y-%m-%d %H:%M:%S %Z')
        error_lines = [
            "==========================================",
            f"Error: Failed to fetch data for plan '{plan}'",
            "==========================================",
            "",
            "Possible reasons:",
            "- The service is temporarily unavailable",
            "- Invalid or expired credentials",
            "- Network connectivity issues",
            "- Plan limits exceeded",
            "",
            f"Timestamp: {current_time}",
            "",
            "Please try again later or contact support.",
            "=========================================="
        ]
        return error_lines
