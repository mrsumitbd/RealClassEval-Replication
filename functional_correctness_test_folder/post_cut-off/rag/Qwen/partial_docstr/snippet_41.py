
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
        sparkles = "✨"
        header_lines = [
            f"{sparkles} Plan: {plan.upper()} {sparkles}",
            f"{sparkles} Timezone: {timezone} {sparkles}",
            f"{sparkles} {'='*30} {sparkles}"
        ]
        return header_lines
