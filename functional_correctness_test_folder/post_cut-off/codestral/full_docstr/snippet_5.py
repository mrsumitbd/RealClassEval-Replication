
import os
import sys
import subprocess
from typing import Dict, Any, Optional
import docker


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
        env_info = {}
        try:
            client = docker.from_env()
            containers = client.containers.list()
            if containers:
                env_info['type'] = 'docker'
                env_info['info'] = str(containers)
            else:
                env_info['type'] = 'system'
                env_info['info'] = 'Running on host system'
        except Exception as e:
            env_info['type'] = 'system'
            env_info['info'] = f'Error checking docker: {str(e)}'
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
        python_version = self._check_python_version()

        with open(log_file, 'w') as log:
            if is_python:
                cmd = [sys.executable, script_path]
            else:
                cmd = [script_path]
            if args:
                cmd.extend(args)

            process = subprocess.Popen(
                cmd, stdout=log, stderr=subprocess.STDOUT)
            result = {
                'pid': process.pid,
                'env_info': env_info,
                'log_file': log_file,
                'python_version': python_version
            }
        return result
