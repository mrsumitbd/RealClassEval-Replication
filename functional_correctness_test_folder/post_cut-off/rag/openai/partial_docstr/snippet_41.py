
class HeaderManager:
    '''Manager for header layout and formatting.'''

    def __init__(self) -> None:
        '''Initialize header manager.'''
        # No state needed for now, but placeholder for future extensions
        pass

    def create_header(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> list[str]:
        '''Create stylized header with sparkles.
        Args:
            plan: Current plan name
            timezone: Display timezone
        Returns:
            List of formatted header lines
        '''
        # Normalise plan name
        plan_name = plan.strip().title()
        tz_name = timezone.strip()

        # Build header lines
        header_lines = [
            "✨" * 30,
            f"✨  Welcome to the {plan_name} Plan!  ✨",
            f"✨  Timezone: {tz_name}  ✨",
            "✨" * 30,
        ]
        return header_lines
