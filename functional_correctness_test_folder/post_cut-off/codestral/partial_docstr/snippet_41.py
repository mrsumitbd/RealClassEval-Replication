
class HeaderManager:
    '''Manager for header layout and formatting.'''

    def __init__(self) -> None:
        self.sparkle = '✨'
        self.border = '=' * 50

    def create_header(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> list[str]:
        '''Create stylized header with sparkles.
        Args:
            plan: Current plan name
            timezone: Display timezone
        Returns:
            List of formatted header lines
        '''
        header_lines = []
        header_lines.append(
            f"{self.sparkle} {plan.upper()} PLAN {self.sparkle}")
        header_lines.append(self.border)
        header_lines.append(f"Timezone: {timezone}")
        header_lines.append(self.border)
        return header_lines
