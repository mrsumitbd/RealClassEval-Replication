
class HeaderManager:
    '''Manager for header layout and formatting.'''

    def __init__(self) -> None:
        '''Initialize header manager.'''
        self.sparkle = '✨'
        self.separator = '─' * 50
        self.plan_colors = {
            'pro': '\033[92m',  # Green
            'basic': '\033[94m',  # Blue
            'premium': '\033[95m',  # Purple
            'default': '\033[93m'  # Yellow
        }
        self.reset_color = '\033[0m'

    def create_header(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> list[str]:
        '''Create stylized header with sparkles.
        Args:
            plan: Current plan name
            timezone: Display timezone
        Returns:
            List of formatted header lines
        '''
        plan_color = self.plan_colors.get(
            plan.lower(), self.plan_colors['default'])
        header_lines = [
            f'{self.sparkle * 3} {plan_color}Plan: {plan.upper()}{self.reset_color} {self.sparkle * 3}',
            f'{self.sparkle} Timezone: {timezone} {self.sparkle}',
            self.separator
        ]
        return header_lines
