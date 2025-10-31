
from __future__ import annotations

import json
import subprocess
from typing import Optional


class ShortcutsCommand:
    """
    A simple command that demonstrates running a shell command and printing
    the result as a dictionary. The command is intentionally minimal and
    can be extended for real shortcut handling.
    """

    def __init__(self) -> None:
        """Initialize the command. No state is required."""
        pass

    def run(self, shell: Optional[str] = None) -> int:
        """
        Execute a simple shell command and print the result.

        Parameters
        ----------
        shell : Optional[str]
            The shell executable to use (e.g., 'bash', 'sh'). If None,
            the default shell from the environment is used.

        Returns
        -------
        int
            The return code of the executed shell command.
        """
        # Determine the shell to use
        shell_exe = shell or subprocess.os.getenv("SHELL", "sh")

        # Build a simple command that echoes a message
        cmd = f"echo 'Hello from {shell_exe}'"

        # Execute the command
        try:
            proc = subprocess.run(
                [shell_exe, "-c", cmd],
                capture_output=True,
                text=True,
                check=False,
            )
        except FileNotFoundError as exc:
            # If the shell executable is not found, report the error
            result = {
                "shell": shell_exe,
                "returncode": -1,
                "stdout": "",
                "stderr": f"Shell not found: {exc}",
            }
            self._print_result(result)
            return -1

        # Prepare the result dictionary
        result = {
            "shell": shell_exe,
            "returncode": proc.returncode,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
        }

        # Print the result
        self._print_result(result)

        return proc.returncode

    def _print_result(self, result: dict) -> None:
        """
        Pretty‑print the result dictionary to stdout.

        Parameters
        ----------
        result : dict
            The dictionary containing command execution details.
        """
        # Use JSON for a clean, readable output
        print(json.dumps(result, indent=2))
