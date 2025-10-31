
import os
import sys
import subprocess
from typing import Dict, Any, Optional


class ScriptRunner:

    def __init__(self, log_path: str = 'data/local_logs/train.log'):
        self.log_path = log_path
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)

    def _prepare_log_file(self, script_type: str) -> str:
        log_file = f"{os.path.splitext(self.log_path)[0]}_{script_type}.log"
        with open(log_file, 'w') as f:
            f.write(f"Log for {script_type} script execution:\n")
        return log_file

    def _check_execution_env(self) -> Dict[str, str]:
        env_info = {
            'platform': sys.platform,
            'python_version': sys.version,
            'cwd': os.getcwd(),
            'path': os.environ['PATH']
        }
        return env_info

    def _check_python_version(self) -> str:
        return sys.version

    def execute_script(self, script_path: str, script_type: str, is_python: bool = False, args: Optional[list] = None) -> Dict[str, Any]:
        log_file = self._prepare_log_file(script_type)
        env_info = self._check_execution_env()
        python_version = self._check_python_version()

        command = [sys.executable, script_path] + (args if args else [])
        if not is_python:
            command = [script_path] + (args if args else [])

        with open(log_file, 'a') as f:
            f.write(f"Environment Info: {env_info}\n")
            f.write(f"Python Version: {python_version}\n")
            f.write(f"Executing command: {' '.join(command)}\n")
            process = subprocess.Popen(command, stdout=f, stderr=f)
            process.wait()

        return {
            'log_file': log_file,
            'exit_code': process.returncode,
            'environment': env_info,
            'python_version': python_version
        }
