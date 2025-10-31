from typing import Final, Sequence

class HeaderManager:
    """Manager for header layout and formatting."""
    DEFAULT_SEPARATOR_CHAR: Final[str] = '='
    DEFAULT_SEPARATOR_LENGTH: Final[int] = 60
    DEFAULT_SPARKLES: Final[str] = '✦ ✧ ✦ ✧'

    def __init__(self) -> None:
        """Initialize header manager."""
        self.separator_char: str = self.DEFAULT_SEPARATOR_CHAR
        self.separator_length: int = self.DEFAULT_SEPARATOR_LENGTH

    def create_header(self, plan: str='pro', timezone: str='Europe/Warsaw') -> list[str]:
        """Create stylized header with sparkles.

        Args:
            plan: Current plan name
            timezone: Display timezone

        Returns:
            List of formatted header lines
        """
        sparkles: str = self.DEFAULT_SPARKLES
        title: str = 'CLAUDE CODE USAGE MONITOR'
        separator: str = self.separator_char * self.separator_length
        return [f'[header]{sparkles}[/] [header]{title}[/] [header]{sparkles}[/]', f'[table.border]{separator}[/]', f'[ {plan.lower()} | {timezone.lower()} ]', '']