
from typing import List


class ErrorDisplayComponent:
    '''Error display component for handling error states.'''

    def __init__(self) -> None:
        # No initialization needed for this simple component
        pass

    def format_error_screen(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> List[str]:
        """
        Return a list of strings representing an error screen.
        The screen includes the plan, timezone, and a generic error message.
        """
        header = "=== ERROR ==="
        plan_line = f"Plan: {plan}"
        timezone_line = f"Timezone: {timezone}"
        message = "An unexpected error has occurred. Please try again later."
        footer = "=== END OF ERROR ==="
        return [header, plan_line, timezone_line, "", message, footer]
