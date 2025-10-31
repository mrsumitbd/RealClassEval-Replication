
class HeaderManager:
    '''Manager for header layout and formatting.'''

    def __init__(self) -> None:
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
            f"{sparkle} Header Manager {sparkle}",
            f"Plan: {plan}",
            f"Timezone: {timezone}",
            f"{sparkle * 20}"
        ]
        return header_lines
