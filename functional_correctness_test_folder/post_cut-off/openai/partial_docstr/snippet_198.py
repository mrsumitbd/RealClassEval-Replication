
import subprocess
from typing import Optional, Dict, Any


class ShortcutsCommand:
    """
    A simple command class for installing and managing shortcuts.
    """

    def __init__(self):
        """初始化快捷键命令"""
        # No special initialization required for this simple implementation.
        pass

    def run(self, shell: Optional[str] = None) -> int:
        """
        安装并管理快捷键

        Parameters
        ----------
        shell : Optional[str]
            The shell command to execute for installing shortcuts. If None,
            a default message will be printed.

        Returns
        -------
        int
            The return code of the executed command (0 for success).
        """
        if shell:
            # Execute the provided shell command and capture its output.
            try:
                completed = subprocess.run(
                    shell,
                    shell=True,
                    capture_output=True,
                    text=True,
                )
                result = {
                    "command": shell,
                    "returncode": completed.returncode,
                    "stdout": completed.stdout.strip(),
                    "stderr": completed.stderr.strip(),
                }
                self._print_result(result)
                return completed.returncode
            except Exception as exc:
                # If an exception occurs, print the error and return a non-zero code.
                result = {
                    "command": shell,
                    "returncode": 1,
                    "stdout": "",
                    "stderr": str(exc),
                }
                self._print_result(result)
                return 1
        else:
            # Default behavior when no shell command is provided.
            message = "No shortcut command specified. Nothing to install."
            print(message)
            return 0

    def _print_result(self, result: Dict[str, Any]) -> None:
        """
        Print the result dictionary in a readable format.

        Parameters
        ----------
        result : dict
            A dictionary containing the command execution details.
        """
        print("Shortcut command execution result:")
        for key, value in result.items():
            print(f"  {key:10s}: {value}")
