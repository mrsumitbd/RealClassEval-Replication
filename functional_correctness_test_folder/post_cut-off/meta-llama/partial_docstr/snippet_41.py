
from datetime import datetime
import pytz


class HeaderManager:
    '''Manager for header layout and formatting.'''

    def __init__(self) -> None:
        self.sparkles = ['*', '+', '#']

    def create_header(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> list[str]:
        '''Create stylized header with sparkles.
        Args:
            plan: Current plan name
            timezone: Display timezone
        Returns:
            List of formatted header lines
        '''
        current_time = datetime.now(pytz.timezone(
            timezone)).strftime('%Y-%m-%d %H:%M:%S')
        header_lines = [
            f"{self.sparkles[0] * 40}",
            f"{self.sparkles[1]} Current Plan: {plan} {self.sparkles[1]}",
            f"{self.sparkles[2]} Time ({timezone}): {current_time} {self.sparkles[2]}",
            f"{self.sparkles[0] * 40}"
        ]
        return header_lines


# Example usage:
if __name__ == "__main__":
    header_manager = HeaderManager()
    header = header_manager.create_header(plan='test', timezone='US/Pacific')
    for line in header:
        print(line)
