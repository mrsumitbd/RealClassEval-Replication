import sys
from typing import Optional, TextIO

class BasicPrinter:
    ERROR = 'ERROR'
    SUCCESS = 'SUCCESS'

    def __init__(self, error: str, success: str, output: Optional[TextIO]=None):
        self.output = output or sys.stdout
        self.success_message = success
        self.error_message = error

    def success(self, message: str) -> None:
        print(self.success_message.format(success=self.SUCCESS, message=message), file=self.output)

    def error(self, message: str) -> None:
        print(self.error_message.format(error=self.ERROR, message=message), file=sys.stderr)

    def diff_line(self, line: str) -> None:
        self.output.write(line)