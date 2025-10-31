
import os
import sys
import subprocess
import datetime
from typing import Any, Dict, List, Optional


class ScriptRunner:
    '''Script executor, supports executing Python and Bash scripts'''

    def __init__(self, log_path: str = 'data/local_logs/train.log'):
        '''
        Initialize script executor
        Args:
            log_path: Base path for log files
        '''
        self.log_path = log_path

    def _prepare_log_file(self, script_type: str) -> str:
        '''
        Prepare log file
        Args:
            script_type: Script type, used for log directory naming
        Returns:
            str: Complete path to the log file
        '''
        base_dir = os.path.dirname(self.log_path)
        log_dir = os.path.join(base_dir, script_type)
        os.makedirs(log_dir, exist_ok=True)
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = os.path.join(log_dir, f'{timestamp}.log')
        return log_file

    def _check_execution_env(self) -> Dict[str, str]:
        '''
        Get current execution environment information, supporting docker or regular system environment
        Returns:
            Dict[str, str]: Dictionary containing environment type and detailed information
        '''
        env_info: Dict[str, str] = {}
        # Detect Docker by presence of /.dockerenv or environment variable
        if os.path.exists('/.dockerenv') or os.getenv('DOCKER', '').lower() == 'true':
            env_info['type'] = 'docker'
            env_info['details'] = 'Running inside Docker container'
        else:
            env_info['type'] = 'host'
            env_info['details'] = 'Running on host system'
        # Add OS info
        try:
            uname = os.uname()
            env_info['os'] = f'{uname.sysname} {uname.release} ({uname.machine})'
        except AttributeError:
            # os.uname may not be available on Windows
            env_info['os'] = sys.platform
        return env_info

    def _check_python_version(self) -> str:
        '''
        Get Python version information
        Returns:
            str: Python version information
        '''
        return sys.version

    def execute_script(
        self,
        script_path: str,
        script_type: str,
        is_python: bool = False,
        args: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
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
        if args is None:
            args = []

        log_file = self._prepare_log_file(script_type)
        env_info = self._check_execution_env()
        python_version = self._check_python_version()

        # Build command
        if is_python:
            cmd = [sys.executable, script_path] + args
        else:
            cmd = ['/bin/bash', script_path] + args

        # Open log file for writing
        with open(log_file, 'w', encoding='utf-8') as lf:
            process = subprocess.Popen(
                cmd,
                stdout=lf,
                stderr=subprocess.STDOUT,
                env=os.environ.copy(),
            )

        result: Dict[str, Any] = {
            'pid': process.pid,
            'env': env_info,
            'log_file': log_file,
            'python_version': python_version,
            'script_path': script_path,
            'script_type': script_type,
            'is_python': is_python,
            'args': args,
        }
        return result
