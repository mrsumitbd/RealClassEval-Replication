
class STMessages:
    """Utility class for displaying styled console messages."""

    # ANSI escape codes for colors
    _RESET = "\033[0m"
    _GREEN = "\033[32m"
    _YELLOW = "\033[33m"
    _RED = "\033[31m"
    _BOLD = "\033[1m"

    def success(self, message: str = 'Operation completed successfully.'):
        """Display a success message."""
        print(f"{self._GREEN}{self._BOLD}{message}{self._RESET}")

    def warning(self, message: str = 'Holy! the dev forgot to write this warning messsage lol 💀.'):
        """Display a warning message."""
        print(f"{self._YELLOW}{self._BOLD}{message}{self._RESET}")

    def error(self, message: str = 'An error occurred.'):
        """Display an error message."""
        print(f"{self._RED}{self._BOLD}{message}{self._RESET}")

    def skull(self, message: str = '💀'):
        """Display a skull message."""
        print(f"{self._BOLD}{message}{self._RESET}")
