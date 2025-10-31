
class HeaderManager:
    '''Manager for header layout and formatting.'''

    def __init__(self) -> None:
        '''Initialize header manager.'''
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
            f"Plan: {plan.upper()}",
            f"Timezone: {timezone}",
            "✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨"
        ]
        return header_lines
