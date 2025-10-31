
import os
import sys
import subprocess
from typing import Dict, Any, Optional
from datetime import datetime


class ScriptRunner:

    def __init__(self, log_path: str = 'data/local_logs/train.log'):

        self.log_path = log_path
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)

    def _prepare_log_file(self, script_type: str) -> str:

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"{self.log_path}.{script_type}.{timestamp}.log"
        return log_file

    def _check_execution_env(self) -> Dict[str, str]:

        env_info = {
            'python_path': sys.executable,
            'python_version': self._check_python_version(),
            'working_directory': os.getcwd(),
            'environment_variables': dict(os.environ)
        }
        return env_info

    def _check_python_version(self) -> str:

        return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

    def execute_script(self, script_path: str, script_type: str, is_python: bool = False, args: Optional[list] = None) -> Dict[str, Any]:

        log_file = self._prepare_log_file(script_type)
        env_info = self._check_execution_env()

        command = [sys.executable, script_path] if is_python else [script_path]
        if args:
            command.extend(args)

        with open(log_file, 'w') as f:
            result = subprocess.run(
                command, stdout=f, stderr=subprocess.STDOUT, text=True)

        execution_info = {
            'script_path': script_path,
            'script_type': script_type,
            'is_python': is_python,
            'args': args,
            'log_file': log_file,
            'return_code': result.returncode,
            'execution_env': env_info
        }

        return execution_info
