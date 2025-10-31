
import os
import subprocess
import sys
from typing import Dict, Any, Optional
import logging
import datetime


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
        log_dir = os.path.dirname(self.log_path)
        log_file_name = f"{script_type}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        log_file_path = os.path.join(log_dir, log_file_name)
        os.makedirs(log_dir, exist_ok=True)
        return log_file_path

    def _check_execution_env(self) -> Dict[str, str]:
        '''
        Get current execution environment information, supporting docker or regular system environment
        Returns:
            Dict[str, str]: Dictionary containing environment type and detailed information
        '''
        env_info = {}
        if os.path.exists('/.dockerenv'):
            env_info['type'] = 'docker'
            env_info['details'] = 'Running inside a Docker container'
        else:
            env_info['type'] = 'system'
            env_info['details'] = f"Running on {sys.platform} system"
        return env_info

    def _check_python_version(self) -> str:
        '''
        Get Python version information
        Returns:
            str: Python version information
        '''
        return f"Python {sys.version}"

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
        log_file_path = self._prepare_log_file(script_type)
        env_info = self._check_execution_env()
        python_version = self._check_python_version()

        if is_python:
            command = [sys.executable, script_path]
        else:
            command = ['bash', script_path]

        if args:
            command.extend(args)

        with open(log_file_path, 'w') as log_file:
            process = subprocess.Popen(
                command, stdout=log_file, stderr=log_file)
            process_id = process.pid

        execution_result = {
            'process_id': process_id,
            'environment_info': env_info,
            'python_version': python_version,
            'log_file_path': log_file_path
        }

        return execution_result


# Example usage
if __name__ == "__main__":
    script_runner = ScriptRunner()
    script_path = 'path_to_your_script.py'  # replace with your script path
    script_type = 'example_script'
    is_python = True
    args = ['--arg1', 'value1']  # replace with your script arguments

    execution_result = script_runner.execute_script(
        script_path, script_type, is_python, args)
    print(execution_result)
