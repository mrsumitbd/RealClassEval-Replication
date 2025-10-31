class HeaderManager:
    '''Manager for header layout and formatting.'''

    def __init__(self) -> None:
        '''Initialize header manager.'''
        self.sparkle = "✨"
        self.line_length = 60

    def create_header(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> list[str]:
        '''Create stylized header with sparkles.
        Args:
            plan: Current plan name
            timezone: Display timezone
        Returns:
            List of formatted header lines
        '''
        header_lines = []
        border = self.sparkle * 2 + " " + \
            ("=" * (self.line_length - 6)) + " " + self.sparkle * 2
        title = f"{self.sparkle}  Welcome to the {plan.capitalize()} Plan  {self.sparkle}"
        title = title.center(self.line_length)
        tz_line = f"Timezone: {timezone}".center(self.line_length)
        header_lines.append(border)
        header_lines.append(title)
        header_lines.append(tz_line)
        header_lines.append(border)
        return header_lines
