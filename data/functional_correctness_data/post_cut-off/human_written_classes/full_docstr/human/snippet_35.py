from claude_monitor.ui.layouts import HeaderManager
from typing import Any, Dict, List, Optional

class ErrorDisplayComponent:
    """Error display component for handling error states."""

    def __init__(self) -> None:
        """Initialize error display component."""

    def format_error_screen(self, plan: str='pro', timezone: str='Europe/Warsaw') -> List[str]:
        """Format error screen for failed data fetch.

        Args:
            plan: Current plan name
            timezone: Display timezone

        Returns:
            List of formatted error screen lines
        """
        screen_buffer = []
        header_manager = HeaderManager()
        screen_buffer.extend(header_manager.create_header(plan, timezone))
        screen_buffer.append('[error]Failed to get usage data[/]')
        screen_buffer.append('')
        screen_buffer.append('[warning]Possible causes:[/]')
        screen_buffer.append("  • You're not logged into Claude")
        screen_buffer.append('  • Network connection issues')
        screen_buffer.append('')
        screen_buffer.append('[dim]Retrying in 3 seconds... (Ctrl+C to exit)[/]')
        return screen_buffer