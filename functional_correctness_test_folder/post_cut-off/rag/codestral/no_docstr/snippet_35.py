
class ErrorDisplayComponent:
    '''Error display component for handling error states.'''

    def __init__(self) -> None:
        '''Initialize error display component.'''
        self.error_message = "Failed to fetch data. Please try again later."
        self.support_email = "support@example.com"
        self.support_phone = "+1 (123) 456-7890"

    def format_error_screen(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> List[str]:
        '''Format error screen for failed data fetch.
        Args:
            plan: Current plan name
            timezone: Display timezone
        Returns:
            List of formatted error screen lines
        '''
        error_screen = [
            "ERROR: Data Fetch Failed",
            "=" * 30,
            "",
            self.error_message,
            "",
            "Current Plan: " + plan,
            "Timezone: " + timezone,
            "",
            "If the problem persists, please contact support:",
            "Email: " + self.support_email,
            "Phone: " + self.support_phone,
            "",
            "=" * 30,
            "Error Code: DATA_FETCH_ERROR"
        ]
        return error_screen
