
from typing import List


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
        error_lines = [
            "Error: Failed to fetch data.",
            f"Plan: {plan}",
            f"Timezone: {timezone}",
            "Please check your network connection and try again.",
            "If the problem persists, contact support."
        ]
        return error_lines
