
class HeaderManager:
    '''Manager for header layout and formatting.'''

    def __init__(self) -> None:
        '''Initialize header manager.'''
        self.sparkle = '✨'

    def create_header(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> list[str]:
        '''Create stylized header with sparkles.
        Args:
            plan: Current plan name
            timezone: Display timezone
        Returns:
            List of formatted header lines
        '''
        header_lines = [
            f"{self.sparkle} {plan.upper()} PLAN {self.sparkle}",
            f"Timezone: {timezone}",
            f"{self.sparkle * (len(plan) + 10)}"
        ]
        return header_lines
