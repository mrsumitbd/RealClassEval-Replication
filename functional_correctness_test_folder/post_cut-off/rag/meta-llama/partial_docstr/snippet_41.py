
from datetime import datetime
import pytz


class HeaderManager:
    """Manager for header layout and formatting."""

    def __init__(self) -> None:
        """Initialize header manager."""
        pass

    def create_header(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> list[str]:
        """Create stylized header with sparkles.

        Args:
            plan: Current plan name
            timezone: Display timezone

        Returns:
            List of formatted header lines
        """
        current_time = datetime.now(pytz.timezone(
            timezone)).strftime('%Y-%m-%d %H:%M:%S %Z%z')
        header_lines = [
            f'****************************************** {plan.upper()} PLAN ******************************************',
            f'*                                                                                                       *',
            f'*  Current Time: {current_time}  *',
            f'*                                                                                                       *',
            f'*********************************************************************************************************'
        ]
        return header_lines
