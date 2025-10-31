
class ErrorDisplayComponent:
    '''Error display component for handling error states.'''

    def __init__(self) -> None:
        '''Initialize error display component.'''
        self.error_message = "Failed to fetch data. Please try again later."
        self.error_code = 500
        self.timestamp = None

    def format_error_screen(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> List[str]:
        '''Format error screen for failed data fetch.
        Args:
            plan: Current plan name
            timezone: Display timezone
        Returns:
            List of formatted error screen lines
        '''
        from datetime import datetime
        import pytz

        self.timestamp = datetime.now(pytz.timezone(
            timezone)).strftime('%Y-%m-%d %H:%M:%S %Z')

        error_screen = [
            f"Error Code: {self.error_code}",
            f"Timestamp: {self.timestamp}",
            f"Plan: {plan}",
            f"Message: {self.error_message}",
            "Please contact support if the issue persists."
        ]

        return error_screen
