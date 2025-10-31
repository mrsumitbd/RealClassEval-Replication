
from typing import List


class ErrorDisplayComponent:
    '''Error display component for handling error states.'''

    def __init__(self) -> None:
        self.error_title = "An error has occurred"
        self.error_message = "We are unable to process your request at this time."
        self.support_contact = "support@example.com"

    def format_error_screen(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> List[str]:
        lines = [
            f"Error: {self.error_title}",
            f"Message: {self.error_message}",
            f"Plan: {plan}",
            f"Timezone: {timezone}",
            f"For assistance, contact: {self.support_contact}"
        ]
        return lines
