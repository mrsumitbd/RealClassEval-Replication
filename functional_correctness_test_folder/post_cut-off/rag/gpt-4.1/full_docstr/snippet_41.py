class HeaderManager:
    '''Manager for header layout and formatting.'''

    def __init__(self) -> None:
        '''Initialize header manager.'''
        self.sparkle = "✨"
        self.header_width = 60

    def create_header(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> list[str]:
        '''Create stylized header with sparkles.
        Args:
            plan: Current plan name
            timezone: Display timezone
        Returns:
            List of formatted header lines
        '''
        lines = []
        border = self.sparkle * 2 + " " + \
            ("=" * (self.header_width - 6)) + " " + self.sparkle * 2
        title = f"Welcome to the {plan.capitalize()} Plan"
        tz_line = f"Timezone: {timezone}"
        # Center the title and timezone line
        title_line = self.sparkle + " " + \
            title.center(self.header_width - 4) + " " + self.sparkle
        tz_line_fmt = self.sparkle + " " + \
            tz_line.center(self.header_width - 4) + " " + self.sparkle
        lines.append(border)
        lines.append(title_line)
        lines.append(tz_line_fmt)
        lines.append(border)
        return lines
