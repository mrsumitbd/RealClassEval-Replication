
import os
import subprocess
import sys
from typing import Any, Dict, Optional
import logging


class ScriptRunner:
    '''Script executor, supports executing Python and Bash scripts'''

    def __init__(self, log_path: str = 'data/local_logs/train.log'):
        '''
        Initialize script executor
        Args:
            log_path: Base path for log files
        '''
        self.log_path = log_path
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def _prepare_log_file(self, script_type: str) -> str:
        '''
        Prepare log file
        Args:
            script_type: Script type, used for log directory naming
        Returns:
            str: Complete path to the log file
        '''
        log_dir = os.path.join(os.path.dirname(self.log_path), script_type)
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, os.path.basename(self.log_path))
        return log_file

    def _check_execution_env(self) -> Dict[str, str]:
        '''
        Get current execution environment information, supporting docker or regular system environment
        Returns:
            Dict[str, str]: Dictionary containing environment type and detailed information
        '''
        env_info = {'type': 'system'}
        if os.path.exists('/.dockerenv'):
            env_info['type'] = 'docker'
        return env_info

    def _check_python_version(self) -> str:
        '''
        Get Python version information
        Returns:
            str: Python version information
        '''
        return sys.version

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
        python_version = self._check_python_version() if is_python else None

        with open(log_file, 'w') as f:
            if is_python:
                command = [sys.executable, script_path] + \
                    (args if args else [])
            else:
                command = [script_path] + (args if args else [])

            process = subprocess.Popen(
                command, stdout=f, stderr=subprocess.STDOUT)
            process.wait()

        return {
            'process_id': process.pid,
            'environment': env_info,
            'python_version': python_version,
            'log_file': log_file
        }
