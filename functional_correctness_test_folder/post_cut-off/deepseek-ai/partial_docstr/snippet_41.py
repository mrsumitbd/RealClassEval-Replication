
class HeaderManager:
    '''Manager for header layout and formatting.'''

    def __init__(self) -> None:
        pass

    def create_header(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> list[str]:
        '''Create stylized header with sparkles.
        Args:
            plan: Current plan name
            timezone: Display timezone
        Returns:
            List of formatted header lines
        '''
        header_lines = [
            "✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨",
            f"Plan: {plan}",
            f"Timezone: {timezone}",
            "✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨"
        ]
        return header_lines
