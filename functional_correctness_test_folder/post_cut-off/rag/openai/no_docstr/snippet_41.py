
class HeaderManager:
    '''Manager for header layout and formatting.'''

    def __init__(self) -> None:
        '''Initialize header manager.'''
        # Default width for the header lines
        self.width = 60
        # Sparkle character to use in the header
        self.sparkle = '✨'

    def create_header(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> list[str]:
        '''Create stylized header with sparkles.
        Args:
            plan: Current plan name
            timezone: Display timezone
        Returns:
            List of formatted header lines
        '''
        # Build the top and bottom border lines
        border = self.sparkle * self.width

        # Prepare the middle lines with plan and timezone centered
        plan_line = f'Plan: {plan}'.center(self.width)
        tz_line = f'Timezone: {timezone}'.center(self.width)

        # Assemble the header
        header = [
            border,
            plan_line,
            tz_line,
            border
        ]

        return header
