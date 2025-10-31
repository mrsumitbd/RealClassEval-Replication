
import os
import sys
import subprocess
from typing import Dict, Any, Optional


class ScriptRunner:

    def __init__(self, log_path: str = 'data/local_logs/train.log'):
        self.log_path = log_path
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

    def _prepare_log_file(self, script_type: str) -> str:
        log_dir = os.path.dirname(self.log_path)
        log_file = os.path.join(log_dir, f"{script_type}.log")
        with open(log_file, 'a') as f:
            f.write(f"=== Starting {script_type} script ===\n")
        return log_file

    def _check_execution_env(self) -> Dict[str, str]:
        env_info = {
            'platform': sys.platform,
            'executable': sys.executable,
            'path': os.getcwd(),
        }
        return env_info

    def _check_python_version(self) -> str:
        return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

    def execute_script(self, script_path: str, script_type: str, is_python: bool = False, args: Optional[list] = None) -> Dict[str, Any]:
        log_file = self._prepare_log_file(script_type)
        env_info = self._check_execution_env()
        py_version = self._check_python_version()

        if args is None:
            args = []

        try:
            if is_python:
                cmd = [sys.executable, script_path] + args
            else:
                cmd = [script_path] + args

            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            with open(log_file, 'a') as f:
                f.write(f"Command: {' '.join(cmd)}\n")
                f.write(f"Stdout:\n{result.stdout}\n")
                f.write(f"Stderr:\n{result.stderr}\n")
                f.write(f"Return code: {result.returncode}\n")

            return {
                'success': result.returncode == 0,
                'return_code': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'env_info': env_info,
                'python_version': py_version,
                'log_file': log_file,
            }
        except Exception as e:
            with open(log_file, 'a') as f:
                f.write(f"Error executing script: {str(e)}\n")

            return {
                'success': False,
                'error': str(e),
                'env_info': env_info,
                'python_version': py_version,
                'log_file': log_file,
            }
