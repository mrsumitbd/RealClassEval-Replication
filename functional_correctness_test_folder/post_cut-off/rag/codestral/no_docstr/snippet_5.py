
import os
import sys
import subprocess
from typing import Dict, Any, Optional
import logging
from datetime import datetime


class ScriptRunner:
    '''Script executor, supports executing Python and Bash scripts'''

    def __init__(self, log_path: str = 'data/local_logs/train.log'):
        '''
        Initialize script executor
        Args:
            log_path: Base path for log files
        '''
        self.log_path = log_path
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

    def _prepare_log_file(self, script_type: str) -> str:
        '''
        Prepare log file
        Args:
            script_type: Script type, used for log directory naming
        Returns:
            str: Complete path to the log file
        '''
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_dir = os.path.join(os.path.dirname(self.log_path), script_type)
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f"{timestamp}.log")
        return log_file

    def _check_execution_env(self) -> Dict[str, str]:
        '''
        Get current execution environment information, supporting docker or regular system environment
        Returns:
            Dict[str, str]: Dictionary containing environment type and detailed information
        '''
        env_info = {}
        if os.path.exists('/.dockerenv'):
            env_info['type'] = 'docker'
            env_info['details'] = 'Running in Docker container'
        else:
            env_info['type'] = 'system'
            env_info['details'] = 'Running on host system'
        return env_info

    def _check_python_version(self) -> str:
        '''
        Get Python version information
        Returns:
            str: Python version information
        '''
        return f"Python {sys.version.split()[0]}"

    def execute_script(self, script_path: str, script_type: str, is_python: bool = False, args: Optional[list] = None) -> Dict[str, Any]:
        '''
        Execute script
        Args:
            script_path: Complete path to the script
            script_type: Script type, used for log directory naming
            is_python: Whether it is a Python script
            args: List of additional script parameters
        Returns:
            Dict[str, Any]: Execution result, including process ID, environment information and log file path
        '''
        log_file = self._prepare_log_file(script_type)
        env_info = self._check_execution_env()
        python_version = self._check_python_version()

        with open(log_file, 'w') as f:
            if is_python:
                command = [sys.executable, script_path]
            else:
                command = [script_path]

            if args:
                command.extend(args)

            process = subprocess.Popen(
                command,
                stdout=f,
                stderr=subprocess.STDOUT,
                text=True
            )

        result = {
            'pid': process.pid,
            'env_info': env_info,
            'python_version': python_version,
            'log_file': log_file,
            'command': ' '.join(command)
        }

        return result
