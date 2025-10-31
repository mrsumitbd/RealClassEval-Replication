
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
        header_lines = []
        sparkle = '✨'
        title = f"{sparkle}  Welcome to Your Dashboard  {sparkle}"
        plan_line = f"Plan: {plan.capitalize()}"
        tz_line = f"Timezone: {timezone}"
        width = max(len(title), len(plan_line), len(tz_line)) + 4
        border = sparkle * (width // len(sparkle))
        header_lines.append(border)
        header_lines.append(title.center(width))
        header_lines.append(plan_line.center(width))
        header_lines.append(tz_line.center(width))
        header_lines.append(border)
        return header_lines
