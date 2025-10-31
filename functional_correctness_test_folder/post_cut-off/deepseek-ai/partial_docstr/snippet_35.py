
from typing import List


class ErrorDisplayComponent:
    '''Error display component for handling error states.'''

    def __init__(self) -> None:
        pass

    def format_error_screen(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> List[str]:
        error_lines = [
            "Error: Unable to process request.",
            f"Plan: {plan}",
            f"Timezone: {timezone}",
            "Please try again later or contact support."
        ]
        return error_lines
