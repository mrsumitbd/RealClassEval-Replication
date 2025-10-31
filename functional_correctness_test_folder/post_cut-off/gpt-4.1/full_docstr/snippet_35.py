
from typing import List


class ErrorDisplayComponent:
    '''Error display component for handling error states.'''

    def __init__(self) -> None:
        '''Initialize error display component.'''
        self.error_title = "Error: Data Fetch Failed"
        self.suggestion = "Please check your network connection or try again later."

    def format_error_screen(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> List[str]:
        '''Format error screen for failed data fetch.
        Args:
            plan: Current plan name
            timezone: Display timezone
        Returns:
            List of formatted error screen lines
        '''
        lines = [
            self.error_title,
            "",
            f"Plan: {plan}",
            f"Timezone: {timezone}",
            "",
            self.suggestion
        ]
        return lines
