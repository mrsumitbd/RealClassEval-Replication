
import os
import subprocess
import sys
import platform
from typing import Dict, Any, Optional


class ScriptRunner:

    def __init__(self, log_path: str = 'data/local_logs/train.log'):
        self.log_path = log_path
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)

    def _prepare_log_file(self, script_type: str) -> str:
        log_dir = os.path.dirname(self.log_path)
        log_file = os.path.join(log_dir, f"{script_type}.log")
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
        else:
            env_info['type'] = 'system'
        env_info['details'] = platform.platform()
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
        Execute a script and return execution details
        Args:
            script_path: Path to the script to execute
            script_type: Type of script (e.g., 'train', 'test')
            is_python: Whether the script is a Python script
            args: Optional list of arguments to pass to the script
        Returns:
            Dict[str, Any]: Dictionary containing execution results and metadata
        '''
        result = {
            'script_path': script_path,
            'script_type': script_type,
            'is_python': is_python,
            'args': args,
            'env_info': self._check_execution_env(),
            'python_version': self._check_python_version(),
            'success': False,
            'output': '',
            'error': ''
        }

        log_file = self._prepare_log_file(script_type)
        command = []

        if is_python:
            command.append(sys.executable)

        command.append(script_path)

        if args:
            command.extend(args)

        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate()

            with open(log_file, 'w') as f:
                f.write(stdout)
                if stderr:
                    f.write("\nERRORS:\n")
                    f.write(stderr)

            result['output'] = stdout
            result['error'] = stderr
            result['success'] = process.returncode == 0
        except Exception as e:
            result['error'] = str(e)

        return result
