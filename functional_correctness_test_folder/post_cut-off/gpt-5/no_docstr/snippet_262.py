class STMessages:
    _COLORS = {
        'success': '\033[92m',  # Green
        'warning': '\033[93m',  # Yellow
        'error': '\033[91m',    # Red
        'skull': '\033[95m',    # Magenta
    }
    _ICONS = {
        'success': '✔️',
        'warning': '⚠️',
        'error': '❌',
        'skull': '💀',
    }
    _RESET = '\033[0m'

    def _format(self, kind: str, message: str) -> str:
        color = self._COLORS.get(kind, '')
        icon = self._ICONS.get(kind, '')
        msg = '' if message is None else str(message)
        return f"{color}{icon} {msg}{self._RESET}"

    def success(self, message: str = 'Operation completed successfully.'):
        return self._format('success', message)

    def warning(self, message: str = 'Holy! the dev forgot to write this warning messsage lol 💀.'):
        return self._format('warning', message)

    def error(self, message: str = 'An error occurred.'):
        return self._format('error', message)

    def skull(self, message: str = '💀'):
        return self._format('skull', message)
