
from typing import List
from datetime import datetime
import pytz


class ErrorDisplayComponent:
    '''Error display component for handling error states.'''

    def __init__(self) -> None:
        '''Initialize error display component.'''
        self.error_messages = {
            'pro': 'Failed to fetch data for PRO plan.',
            'basic': 'Failed to fetch data for BASIC plan.',
            'default': 'Failed to fetch data.'
        }

    def format_error_screen(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> List[str]:
        '''Format error screen for failed data fetch.
        Args:
            plan: Current plan name
            timezone: Display timezone
        Returns:
            List of formatted error screen lines
        '''
        error_message = self.error_messages.get(
            plan.lower(), self.error_messages['default'])
        current_time = datetime.now(pytz.timezone(
            timezone)).strftime('%Y-%m-%d %H:%M:%S %Z%z')

        error_screen = [
            '------------------------',
            '         ERROR          ',
            '------------------------',
            error_message,
            f'Timezone: {timezone}',
            f'Current Time: {current_time}',
            '------------------------'
        ]

        return error_screen


# Example usage:
if __name__ == "__main__":
    error_display = ErrorDisplayComponent()
    print(error_display.format_error_screen('pro'))
    print(error_display.format_error_screen('basic', 'America/New_York'))
