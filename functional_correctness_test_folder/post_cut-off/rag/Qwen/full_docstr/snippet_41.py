
class HeaderManager:
    '''Manager for header layout and formatting.'''

    def __init__(self) -> None:
        '''Initialize header manager.'''
        self.sparkles = ['✨', '💫', '🌟', '💥', '⚡']

    def create_header(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> list[str]:
        '''Create stylized header with sparkles.
        Args:
            plan: Current plan name
            timezone: Display timezone
        Returns:
            List of formatted header lines
        '''
        sparkle = self.sparkles[hash(plan) % len(self.sparkles)]
        header_lines = [
            f"{sparkle} Plan: {plan.upper()} {sparkle}",
            f"Timezone: {timezone}",
            f"{sparkle * 10}"
        ]
        return header_lines
