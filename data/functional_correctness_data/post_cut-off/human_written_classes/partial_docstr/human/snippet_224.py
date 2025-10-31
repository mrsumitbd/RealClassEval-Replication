from io import StringIO
import types
import sys
from typing import Any, Callable, Dict, List, Optional, Type

class OutputCapture:
    """Captures stdout and stderr output."""

    def __init__(self) -> None:
        self.stdout = StringIO()
        self.stderr = StringIO()
        self._stdout = sys.stdout
        self._stderr = sys.stderr

    def __enter__(self) -> 'OutputCapture':
        sys.stdout = self.stdout
        sys.stderr = self.stderr
        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException], traceback: Optional[types.TracebackType]) -> None:
        sys.stdout = self._stdout
        sys.stderr = self._stderr

    def get_output(self) -> str:
        """Get captured output from both stdout and stderr."""
        output = self.stdout.getvalue()
        errors = self.stderr.getvalue()
        if errors:
            output += f'\nErrors:\n{errors}'
        return output