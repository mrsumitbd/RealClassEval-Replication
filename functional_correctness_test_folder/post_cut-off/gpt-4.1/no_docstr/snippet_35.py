
from typing import List


class ErrorDisplayComponent:

    def __init__(self) -> None:
        pass

    def format_error_screen(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> List[str]:
        lines = [
            f"Error: Unable to load data.",
            f"Plan: {plan.capitalize()}",
            f"Timezone: {timezone}",
            "Please try again later or contact support."
        ]
        return lines
