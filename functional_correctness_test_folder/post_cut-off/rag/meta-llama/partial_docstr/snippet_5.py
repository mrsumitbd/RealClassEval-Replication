
import os
import subprocess
import sys
from typing import Any, Dict, List, Optional
import logging
import uuid


class ScriptRunner:
    """Script executor, supports executing Python and Bash scripts"""

    def __init__(self, log_path: str = 'data/local_logs/train.log'):
        """
        Initialize script executor

        Args:
            log_path: Base path for log files
        """
        self.log_path = log_path

    def _prepare_log_file(self, script_type: str) -> str:
        """
        Prepare log file

        Args:
            script_type: Script type, used for log directory naming

        Returns:
            str: Complete path to the log file
        """
        log_dir = os.path.join(os.path.dirname(self.log_path), script_type)
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f'{uuid.uuid4()}.log')
        return log_file

    def _check_execution_env(self) -> Dict[str, str]:
        """
        Get current execution environment information, supporting docker or regular system environment

        Returns:
            Dict[str, str]: Dictionary containing environment type and detailed information
        """
        env_info = {}
        if os.path.exists('/.dockerenv'):
            env_info['type'] = 'docker'
            env_info['info'] = 'Running inside Docker container'
        else:
            env_info['type'] = 'system'
            env_info['info'] = f'Running on {sys.platform} system'
        return env_info

    def _check_python_version(self) -> str:
        """
        Get Python version information

        Returns:
            str: Python version information
        """
        return f'Python {sys.version}'

    def execute_script(self, script_path: str, script_type: str, is_python: bool = False, args: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Execute script

        Args:
            script_path: Complete path to the script
            script_type: Script type, used for log directory naming
            is_python: Whether it is a Python script
            args: List of additional script parameters

        Returns:
            Dict[str, Any]: Execution result, including process ID, environment information and log file path
        """
        log_file = self._prepare_log_file(script_type)
        env_info = self._check_execution_env()
        python_version = self._check_python_version()

        if is_python:
            command = [sys.executable, script_path]
        else:
            command = [script_path]

        if args:
            command.extend(args)

        with open(log_file, 'w') as f:
            process = subprocess.Popen(command, stdout=f, stderr=f)
            pid = process.pid
            process.wait()
            returncode = process.returncode

        execution_result = {
            'pid': pid,
            'env_info': env_info,
            'python_version': python_version,
            'log_file': log_file,
            'returncode': returncode
        }

        if returncode != 0:
            logging.error(
                f'Script {script_path} failed with return code {returncode}. See {log_file} for details.')
        else:
            logging.info(
                f'Script {script_path} executed successfully. See {log_file} for details.')

        return execution_result
