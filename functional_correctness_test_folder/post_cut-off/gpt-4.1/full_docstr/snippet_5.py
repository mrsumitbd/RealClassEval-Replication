
import os
import sys
import subprocess
import datetime
from typing import Dict, Any, Optional


class ScriptRunner:
    '''Script executor, supports executing Python and Bash scripts'''

    def __init__(self, log_path: str = 'data/local_logs/train.log'):
        '''
        Initialize script executor
        Args:
            log_path: Base path for log files
        '''
        self.base_log_path = log_path

    def _prepare_log_file(self, script_type: str) -> str:
        '''
        Prepare log file
        Args:
            script_type: Script type, used for log directory naming
        Returns:
            str: Complete path to the log file
        '''
        base_dir = os.path.dirname(self.base_log_path)
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
        env_info = {}
        # Check for Docker by looking for /.dockerenv or cgroup info
        if os.path.exists('/.dockerenv'):
            env_info['env_type'] = 'docker'
            env_info['detail'] = 'Detected /.dockerenv file'
        else:
            try:
                with open('/proc/1/cgroup', 'rt') as f:
                    content = f.read()
                if 'docker' in content or 'containerd' in content:
                    env_info['env_type'] = 'docker'
                    env_info['detail'] = 'Detected docker/containerd in /proc/1/cgroup'
                else:
                    env_info['env_type'] = 'system'
                    env_info['detail'] = 'No docker indicators found'
            except Exception:
                env_info['env_type'] = 'system'
                env_info['detail'] = 'Could not read /proc/1/cgroup'
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
        cmd = []
        if is_python:
            cmd = [sys.executable, script_path]
        else:
            cmd = ['bash', script_path]
        if args:
            cmd += args

        with open(log_file, 'w') as lf:
            try:
                proc = subprocess.Popen(
                    cmd,
                    stdout=lf,
                    stderr=subprocess.STDOUT
                )
                proc.wait()
                result = {
                    'pid': proc.pid,
                    'returncode': proc.returncode,
                    'env_info': self._check_execution_env(),
                    'python_version': self._check_python_version() if is_python else None,
                    'log_file': log_file,
                    'success': proc.returncode == 0
                }
            except Exception as e:
                result = {
                    'pid': None,
                    'returncode': None,
                    'env_info': self._check_execution_env(),
                    'python_version': self._check_python_version() if is_python else None,
                    'log_file': log_file,
                    'success': False,
                    'error': str(e)
                }
        return result
