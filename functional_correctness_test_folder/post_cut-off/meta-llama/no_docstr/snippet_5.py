
import os
import sys
import subprocess
from typing import Dict, Any, Optional
import logging


class ScriptRunner:

    def __init__(self, log_path: str = 'data/local_logs/train.log'):
        self.log_path = log_path

    def _prepare_log_file(self, script_type: str) -> str:
        log_dir = os.path.dirname(self.log_path)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_file = f"{self.log_path}.{script_type}"
        if os.path.exists(log_file):
            os.remove(log_file)
        return log_file

    def _check_execution_env(self) -> Dict[str, str]:
        env_vars = os.environ.copy()
        return env_vars

    def _check_python_version(self) -> str:
        return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

    def execute_script(self, script_path: str, script_type: str, is_python: bool = False, args: Optional[list] = None) -> Dict[str, Any]:
        log_file = self._prepare_log_file(script_type)
        env_vars = self._check_execution_env()
        python_version = self._check_python_version()

        if is_python:
            command = [sys.executable, script_path]
        else:
            command = [script_path]

        if args is not None:
            command.extend(args)

        try:
            with open(log_file, 'w') as f:
                subprocess.run(command, env=env_vars,
                               stdout=f, stderr=f, check=True)
            execution_status = "success"
        except subprocess.CalledProcessError as e:
            execution_status = "failed"
            logging.error(
                f"Script execution failed with return code {e.returncode}")

        execution_result = {
            "log_file": log_file,
            "execution_status": execution_status,
            "python_version": python_version,
            "command": ' '.join(command)
        }
        return execution_result
