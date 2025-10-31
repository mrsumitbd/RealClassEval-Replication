import os
from typing import Any, Dict, List, Literal, Tuple, Union

class CommandContext:
    """Maintains command execution context including working directory."""

    def __init__(self, base_dir: str) -> None:
        self.base_dir = os.path.abspath(base_dir)
        self.current_dir = self.base_dir
        self._dir_stack: List[str] = []

    def push_dir(self) -> None:
        """Save current directory to stack."""
        self._dir_stack.append(self.current_dir)

    def pop_dir(self) -> None:
        """Restore previous directory from stack."""
        if self._dir_stack:
            self.current_dir = self._dir_stack.pop()

    def update_dir(self, command: str) -> None:
        """Update current directory based on cd command."""
        if command.strip().startswith('cd '):
            new_dir = command.split('cd ', 1)[1].strip()
            if new_dir.startswith('/'):
                self.current_dir = os.path.abspath(new_dir)
            else:
                self.current_dir = os.path.abspath(os.path.join(self.current_dir, new_dir))