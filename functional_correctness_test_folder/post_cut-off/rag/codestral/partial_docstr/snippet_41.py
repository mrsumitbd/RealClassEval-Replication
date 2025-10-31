
class HeaderManager:
    '''Manager for header layout and formatting.'''

    def __init__(self) -> None:
        '''Initialize header manager.'''
        self.sparkle = '✨'
        self.separator = '─' * 50
        self.plan_colors = {
            'pro': '\033[94m',  # Blue
            'basic': '\033[92m',  # Green
            'premium': '\033[95m',  # Purple
            'free': '\033[93m'  # Yellow
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
        header_lines = []
        plan_color = self.plan_colors.get(plan.lower(), self.reset_color)

        # Top border
        header_lines.append(
            f'{self.sparkle * 2} {self.separator} {self.sparkle * 2}')

        # Title line
        title = f'{" " * 10}Welcome to Your Dashboard!{" " * 10}'
        header_lines.append(f'{self.sparkle} {title} {self.sparkle}')

        # Plan information
        plan_info = f'{" " * 12}Current Plan: {plan_color}{plan.upper()}{self.reset_color}{" " * 12}'
        header_lines.append(f'{self.sparkle} {plan_info} {self.sparkle}')

        # Timezone information
        timezone_info = f'{" " * 12}Timezone: {timezone}{" " * 12}'
        header_lines.append(f'{self.sparkle} {timezone_info} {self.sparkle}')

        # Bottom border
        header_lines.append(
            f'{self.sparkle * 2} {self.separator} {self.sparkle * 2}')

        return header_lines
