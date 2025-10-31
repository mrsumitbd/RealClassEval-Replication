import sys
from typing import Any
import os

class TerminalInputManager:
    """
    Terminal Manager inspired by: https://simondlevy.academic.wlu.edu/files/software/kbhit.py
    """
    fd: int
    new_term: list
    old_term: list
    is_interactive: bool = False

    def __init__(self) -> None:
        self.is_interactive = sys.stdin.isatty() and os.isatty(sys.stdin.fileno())

    def __enter__(self) -> 'TerminalInputManager':
        if not self.is_interactive:
            return self
        if sys.platform == 'win32':
            pass
        else:
            try:
                self.fd = sys.stdin.fileno()
                self.new_term = termios.tcgetattr(self.fd)
                self.old_term = termios.tcgetattr(self.fd)
                self.new_term[3] = self.new_term[3] & ~termios.ICANON & ~termios.ECHO
                termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)
            except termios.error:
                self.is_interactive = False
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if not self.is_interactive:
            return
        if sys.platform != 'win32':
            try:
                termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)
            except termios.error:
                pass

    def get_char(self, block: bool) -> str | None:
        """Get a single character

        Parameters
        ----------
        block: bool
            Whether the function should block until a character is received.

        Returns
        -------
        str | None
            The character received, or None if no character was received and block is False.
        """
        if sys.platform == 'win32':
            if block:
                return msvcrt.getch().decode('utf-8')
            elif msvcrt.kbhit():
                return msvcrt.getch().decode('utf-8')
        elif block:
            return sys.stdin.read(1)
        else:
            i, _, _ = select.select([sys.stdin], [], [], 0)
            if i != []:
                return sys.stdin.read(1)
        return None