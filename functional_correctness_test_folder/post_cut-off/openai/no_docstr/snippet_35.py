
from typing import List


class ErrorDisplayComponent:
    def __init__(self) -> None:
        # Default error message that can be overridden if needed
        self._error_message = "An unexpected error occurred."

    def format_error_screen(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> List[str]:
        """
        Return a formatted error screen as a list of strings.

        Parameters
        ----------
        plan : str, optional
            The subscription plan to display (default is 'pro').
        timezone : str, optional
            The timezone to display (default is 'Europe/Warsaw').

        Returns
        -------
        List[str]
            A list of strings representing the formatted error screen.
        """
        header = f"=== ERROR SCREEN ({plan.upper()}) ==="
        time_info = f"Timezone: {timezone}"
        body = self._error_message
        footer = "Please contact support."

        return [header, time_info, "", body, "", footer]
