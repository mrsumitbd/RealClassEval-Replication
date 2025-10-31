
from typing import List
from datetime import datetime
import pytz


class ErrorDisplayComponent:
    '''Error display component for handling error states.'''

    def __init__(self) -> None:
        self.error_messages = {
            'pro': 'An error occurred. Please try again later.',
            'basic': 'Error. Please contact support.'
        }
        self.support_info = {
            'email': 'support@example.com',
            'phone': '+48 123 456 789'
        }

    def format_error_screen(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> List[str]:
        error_message = self.error_messages.get(plan, 'An error occurred.')
        current_time = datetime.now(pytz.timezone(
            timezone)).strftime('%Y-%m-%d %H:%M:%S %Z%z')
        error_screen = [
            f'Error Screen - {current_time}',
            '-' * 50,
            error_message,
            '-' * 50,
            'For assistance, please contact:',
            f'Email: {self.support_info["email"]}',
            f'Phone: {self.support_info["phone"]}'
        ]
        return error_screen


# Example usage:
if __name__ == "__main__":
    error_display = ErrorDisplayComponent()
    print(error_display.format_error_screen())
