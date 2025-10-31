
from typing import List
from datetime import datetime
import pytz


class ErrorDisplayComponent:

    def __init__(self) -> None:
        self.error_messages = {
            'pro': {
                'header': 'Error Occurred',
                'message': 'An unexpected error occurred. Please try again later.'
            },
            'basic': {
                'header': 'Error',
                'message': 'Something went wrong. Please contact support.'
            }
        }

    def format_error_screen(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> List[str]:
        error_info = self.error_messages.get(plan, self.error_messages['pro'])
        current_time = datetime.now(pytz.timezone(
            timezone)).strftime('%Y-%m-%d %H:%M:%S %Z%z')

        error_screen = [
            f"### {error_info['header']} ###",
            error_info['message'],
            f"Time: {current_time}",
            "Please try again or contact support if the issue persists."
        ]

        return error_screen


# Example usage:
if __name__ == "__main__":
    error_display = ErrorDisplayComponent()
    print(error_display.format_error_screen('pro'))
    print(error_display.format_error_screen('basic'))
    print(error_display.format_error_screen())
