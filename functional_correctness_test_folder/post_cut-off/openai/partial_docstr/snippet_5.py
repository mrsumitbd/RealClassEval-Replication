
import os
import sys
import subprocess
import platform
import datetime
from typing import Dict, Any, Optional, List


class ScriptRunner:
    """
    A utility class to execute scripts (Python or shell) and log their output.
    """

    def __init__(self, log_path: str = 'data/local_logs/train.log'):
        """
        Initialize the ScriptRunner.

        Parameters
        ----------
        log_path : str, optional
            Base path for log files. Defaults to 'data/local_logs/train.log'.
        """
        self.log_path = log_path
        # Ensure the directory for logs exists
        log_dir = os.path.dirname(self.log_path)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

    def _prepare_log_file(self, script_type: str) -> str:
        """
        Prepare a log file path based on script type and current timestamp.

        Parameters
        ----------
        script_type : str
            Type of the script (e.g., 'python', 'bash').

        Returns
        -------
        str
            Full path to the log file.
        """
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        base, ext = os.path.splitext(self.log_path)
        log_file = f"{base}_{script_type}_{timestamp}.log"
        return log_file

    def _check_execution_env(self) -> Dict[str, str]:
        """
        Get current execution environment information, supporting Docker or regular system environment.

        Returns
        -------
        Dict[str, str]
            Dictionary containing environment type and detailed information.
        """
        env_info: Dict[str, str] = {}

        # Detect Docker
        in_docker = False
        if os.path.exists('/.dockerenv'):
            in_docker = True
        else:
            try:
                with open('/proc/self/cgroup', 'r') as f:
                    for line in f:
                        if 'docker' in line or 'kubepods' in line:
                            in_docker = True
                            break
            except Exception:
                pass

        env_info['environment'] = 'docker' if in_docker else 'host'
        env_info['platform'] = platform.platform()
        env_info['python_version'] = sys.version
        return env_info

    def _check_python_version(self) -> str:
        """
        Get Python version information.

        Returns
        -------
        str
            Python version information.
        """
        return sys.version

    def execute_script(
        self,
        script_path: str,
        script_type: str,
        is_python: bool = False,
        args: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Execute a script and log its output.

        Parameters
        ----------
        script_path : str
            Path to the script to execute.
        script_type : str
            Type of the script (used for log naming).
        is_python : bool, optional
            Whether the script is a Python script. Defaults to False.
        args : Optional[list], optional
            Additional arguments to pass to the script. Defaults to None.

        Returns
        -------
        Dict[str, Any]
            Dictionary containing execution results and logs.
        """
        if args is None:
            args = []

        # Prepare log file
        log_file = self._prepare_log_file(script_type)

        # Build command
        if is_python:
            cmd = [sys.executable, script_path] + args
        else:
            # Assume shell script; use sh -c
            cmd = ['sh', script_path] + args

        # Execute
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False
            )
            success = result.returncode == 0
        except Exception as e:
            result = None
            success = False
            error_msg = str(e)

        # Write logs
        try:
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write(f"Command: {' '.join(cmd)}\n")
                f.write(
                    f"Return Code: {result.returncode if result else 'N/A'}\n")
                f.write("=== STDOUT ===\n")
                f.write(result.stdout if result else '')
                f.write("\n=== STDERR ===\n")
                f.write(result.stderr if result else '')
                if not success and result is None:
                    f.write(f"\nError: {error_msg}\n")
        except Exception as e:
            # If logging fails, we still return the execution result
            pass

        return {
            'success': success,
            'returncode': result.returncode if result else None,
            'stdout': result.stdout if result else '',
            'stderr': result.stderr if result else '',
            'log_file': log_file,
            'env': self._check_execution_env(),
            'python_version': self._check_python_version()
        }
