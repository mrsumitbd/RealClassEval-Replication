
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
        # Sparkle unicode
        sparkle = '✨'
        # Compose header lines
        header_lines = [
            f"{sparkle*3}  Welcome to the Dashboard  {sparkle*3}",
            f"Plan: {plan.capitalize()}",
            f"Timezone: {timezone}",
            f"{sparkle*13}"
        ]
        return header_lines
