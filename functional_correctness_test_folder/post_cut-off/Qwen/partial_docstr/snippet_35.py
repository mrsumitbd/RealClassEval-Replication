
from typing import List


class ErrorDisplayComponent:
    '''Error display component for handling error states.'''

    def __init__(self) -> None:
        self.error_messages = {
            'pro': "An error occurred in your Pro plan. Please contact support.",
            'basic': "An error occurred in your Basic plan. Please contact support.",
            'free': "An error occurred in your Free plan. Please contact support."
        }
        self.timezone = timezone

    def format_error_screen(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> List[str]:
        self.timezone = timezone
        error_message = self.error_messages.get(
            plan, "An unknown error occurred. Please contact support.")
        return [f"Error in {plan} plan", error_message, f"Timezone: {self.timezone}"]
