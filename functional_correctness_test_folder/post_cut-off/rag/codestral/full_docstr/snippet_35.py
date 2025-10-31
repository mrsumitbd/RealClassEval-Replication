
class ErrorDisplayComponent:
    '''Error display component for handling error states.'''

    def __init__(self) -> None:
        '''Initialize error display component.'''
        self.error_message = "Failed to fetch data. Please try again later."
        self.support_message = "If the problem persists, contact support."

    def format_error_screen(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> List[str]:
        '''Format error screen for failed data fetch.
        Args:
            plan: Current plan name
            timezone: Display timezone
        Returns:
            List of formatted error screen lines
        '''
        error_screen = [
            f"Error: {self.error_message}",
            f"Plan: {plan}",
            f"Timezone: {timezone}",
            f"Support: {self.support_message}"
        ]
        return error_screen
