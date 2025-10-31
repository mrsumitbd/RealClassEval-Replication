
class HeaderManager:
    '''Manager for header layout and formatting.'''

    def __init__(self) -> None:
        '''Initialize header manager.'''
        self._sparkle = "✨"

    def create_header(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> list[str]:
        '''Create stylized header with sparkles.
        Args:
            plan: Current plan name
            timezone: Display timezone
        Returns:
            List of formatted header lines
        '''
        header_lines = [
            f"{self._sparkle} Welcome to the {plan.capitalize()} Plan {self._sparkle}",
            f"{self._sparkle} Timezone: {timezone} {self._sparkle}",
            f"{self._sparkle} Enjoy your stay! {self._sparkle}"
        ]
        return header_lines
