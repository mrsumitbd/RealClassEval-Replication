
from datetime import datetime
import pytz


class HeaderManager:
    '''Manager for header layout and formatting.'''

    def __init__(self) -> None:
        '''Initialize header manager.'''
        self.sparkle_chars = ['*', '+', '#']

    def create_header(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> list[str]:
        '''Create stylized header with sparkles.
        Args:
            plan: Current plan name
            timezone: Display timezone
        Returns:
            List of formatted header lines
        '''
        current_time = datetime.now(pytz.timezone(
            timezone)).strftime('%Y-%m-%d %H:%M:%S %Z%z')
        header_lines = [
            f"{self.sparkle_chars[0] * 40}",
            f"*{' ' * 38}*",
            f"*{'Current Plan: ' + plan:^36}*",
            f"*{' ' * 38}*",
            f"*{'Current Time: ' + current_time:^36}*",
            f"*{' ' * 38}*",
            f"{self.sparkle_chars[0] * 40}",
        ]
        return header_lines


# Example usage:
if __name__ == "__main__":
    header_manager = HeaderManager()
    header = header_manager.create_header(plan='pro', timezone='US/Pacific')
    for line in header:
        print(line)
