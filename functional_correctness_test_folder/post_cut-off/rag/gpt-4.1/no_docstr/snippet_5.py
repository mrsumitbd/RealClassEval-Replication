
import os
import sys
import subprocess
import datetime
from typing import Dict, Any, Optional, List


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
        log_file = os.path.join(log_dir, f"{timestamp}.log")
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
                    cgroup_content = f.read()
                if 'docker' in cgroup_content or 'containerd' in cgroup_content:
                    env_info['env_type'] = 'docker'
                    env_info['detail'] = 'Found docker/containerd in /proc/1/cgroup'
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
        return sys.version.replace('\n', ' ')

    def execute_script(self, script_path: str, script_type: str, is_python: bool = False, args: Optional[List] = None) -> Dict[str, Any]:
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
        cmd = []
        if is_python:
            cmd = [sys.executable, script_path]
        else:
            cmd = ['bash', script_path]
        if args:
            cmd += list(map(str, args))
        with open(log_file, 'w') as lf:
            lf.write(f"=== ScriptRunner Execution Log ===\n")
            lf.write(f"Time: {datetime.datetime.now()}\n")
            lf.write(f"Script: {script_path}\n")
            lf.write(f"Type: {script_type}\n")
            lf.write(f"Python Version: {python_version}\n")
            lf.write(f"Environment: {env_info}\n")
            lf.write(f"Command: {' '.join(cmd)}\n")
            lf.write(f"===============================\n\n")
            try:
                proc = subprocess.Popen(
                    cmd,
                    stdout=lf,
                    stderr=subprocess.STDOUT,
                    env=os.environ.copy()
                )
                proc.wait()
                return {
                    'pid': proc.pid,
                    'returncode': proc.returncode,
                    'env_info': env_info,
                    'python_version': python_version,
                    'log_file': log_file,
                    'success': proc.returncode == 0
                }
            except Exception as e:
                lf.write(f"\n[ERROR] Exception occurred: {e}\n")
                return {
                    'pid': None,
                    'returncode': None,
                    'env_info': env_info,
                    'python_version': python_version,
                    'log_file': log_file,
                    'success': False,
                    'error': str(e)
                }
