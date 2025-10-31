
from datetime import datetime
import pytz


class HeaderManager:

    def __init__(self) -> None:
        """
        Initialize the HeaderManager class.
        """
        pass

    def create_header(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> list[str]:
        """
        Creates a header based on the given plan and timezone.

        Args:
        plan (str): The plan type. Defaults to 'pro'.
        timezone (str): The timezone. Defaults to 'Europe/Warsaw'.

        Returns:
        list[str]: A list of header strings.
        """
        # Get the current date and time in the specified timezone
        tz = pytz.timezone(timezone)
        current_datetime = datetime.now(tz)

        # Format the date and time
        date_str = current_datetime.strftime('%Y-%m-%d')
        time_str = current_datetime.strftime('%H:%M:%S')

        # Create the header based on the plan
        if plan.lower() == 'pro':
            header = [
                f'Date: {date_str}', f'Time ({timezone}): {time_str}', 'Plan: Professional']
        elif plan.lower() == 'basic':
            header = [f'Date: {date_str}',
                      f'Time ({timezone}): {time_str}', 'Plan: Basic']
        else:
            header = [
                f'Date: {date_str}', f'Time ({timezone}): {time_str}', f'Plan: {plan.capitalize()}']

        return header


# Example usage:
if __name__ == "__main__":
    header_manager = HeaderManager()
    print(header_manager.create_header('pro'))
    print(header_manager.create_header('basic'))
    print(header_manager.create_header('custom'))
