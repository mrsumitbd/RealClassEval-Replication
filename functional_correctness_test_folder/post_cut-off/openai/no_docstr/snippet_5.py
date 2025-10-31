
import os
import sys
import subprocess
import datetime
from typing import Dict, Any, Optional, List


class ScriptRunner:
    def __init__(self, log_path: str = 'data/local_logs/train.log'):
        """
        Initialize the ScriptRunner with a default log path.
        The directory for the log file is created if it does not exist.
        """
        self.log_path = log_path
        log_dir = os.path.dirname(self.log_path)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

    def _prepare_log_file(self, script_type: str) -> str:
        """
        Create a log file name based on the script type and current timestamp.
        The log file is placed in the same directory as the default log path.
        """
        base_dir = os.path.dirname(self.log_path)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file_name = f"{script_type}_{timestamp}.log"
        return os.path.join(base_dir, log_file_name)

    def _check_execution_env(self) -> Dict[str, str]:
        """
        Return a dictionary of relevant environment variables for the execution context.
        """
        env_vars = {
            "PATH": os.getenv("PATH", ""),
            "PYTHONPATH": os.getenv("PYTHONPATH", ""),
            "HOME": os.getenv("HOME", ""),
            "USER": os.getenv("USER", ""),
        }
        return env_vars

    def _check_python_version(self) -> str:
        """
        Return the current Python interpreter version as a string.
        """
        return sys.version

    def execute_script(
        self,
        script_path: str,
        script_type: str,
        is_python: bool = False,
        args: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Execute a script located at `script_path`. If `is_python` is True, the script
        is executed with the current Python interpreter; otherwise it is executed
        directly (e.g., a shell script). Additional command-line arguments can be
        passed via `args`.

        Returns a dictionary containing:
            - success (bool)
            - stdout (str)
            - stderr (str)
            - exit_code (int)
            - env (dict)
            - python_version (str)
            - log_file (str)
        """
        if args is None:
            args = []

        # Prepare the command
        if is_python:
            cmd = [sys.executable, script_path] + args
        else:
            cmd = [script_path] + args

        # Prepare logging
        log_file = self._prepare_log_file(script_type)

        # Execute the script
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                env=os.environ,
                check=False,
            )
            success = result.returncode == 0
        except Exception as e:
            # In case of an exception, capture the error message
            result = subprocess.CompletedProcess(
                args=cmd,
                returncode=1,
                stdout="",
                stderr=str(e),
            )
            success = False

        # Write logs
        with open(log_file, "w", encoding="utf-8") as f:
            f.write(f"Command: {' '.join(result.args)}\n")
            f.write(f"Return code: {result.returncode}\n")
            f.write("\n--- STDOUT ---\n")
            f.write(result.stdout or "")
            f.write("\n--- STDERR ---\n")
            f.write(result.stderr or "")

        # Assemble the result dictionary
        output = {
            "success": success,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode,
            "env": self._check_execution_env(),
            "python_version": self._check_python_version(),
            "log_file": log_file,
        }

        return output
