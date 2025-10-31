
from typing import List


class ErrorDisplayComponent:

    def __init__(self) -> None:
        pass

    def format_error_screen(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> List[str]:
        error_screen = [
            "Error: Something went wrong.",
            f"Plan: {plan}",
            f"Timezone: {timezone}"
        ]
        return error_screen
