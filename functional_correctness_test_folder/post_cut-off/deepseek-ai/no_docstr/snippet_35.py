
from typing import List


class ErrorDisplayComponent:

    def __init__(self) -> None:
        pass

    def format_error_screen(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> List[str]:
        error_lines = [
            "ERROR SCREEN",
            f"Plan: {plan}",
            f"Timezone: {timezone}",
            "An unexpected error occurred.",
            "Please try again later."
        ]
        return error_lines
