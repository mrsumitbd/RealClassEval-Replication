
import os
import sys
import subprocess
from typing import Dict, Any, Optional
import docker


class ScriptRunner:

    def __init__(self, log_path: str = 'data/local_logs/train.log'):

        self.log_path = log_path
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

    def _prepare_log_file(self, script_type: str) -> str:

        log_file = f"{self.log_path}.{script_type}"
        with open(log_file, 'w') as f:
            pass
        return log_file

    def _check_execution_env(self) -> Dict[str, str]:

        env_info = {}
        try:
            client = docker.from_env()
            env_info['type'] = 'docker'
            env_info['info'] = str(client.info())
        except:
            env_info['type'] = 'system'
            env_info['info'] = 'Regular system environment'
        return env_info

    def _check_python_version(self) -> str:

        return sys.version

    def execute_script(self, script_path: str, script_type: str, is_python: bool = False, args: Optional[list] = None) -> Dict[str, Any]:

        result = {}
        log_file = self._prepare_log_file(script_type)
        env_info = self._check_execution_env()
        python_version = self._check_python_version()

        result['log_file'] = log_file
        result['env_info'] = env_info
        result['python_version'] = python_version

        with open(log_file, 'a') as f:
            f.write(f"Environment: {env_info}\n")
            f.write(f"Python Version: {python_version}\n")

            if is_python:
                command = [sys.executable, script_path]
            else:
                command = [script_path]

            if args:
                command.extend(args)

            process = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            result['return_code'] = process.returncode
            result['stdout'] = stdout.decode('utf-8')
            result['stderr'] = stderr.decode('utf-8')

            f.write(f"Command: {' '.join(command)}\n")
            f.write(f"Return Code: {process.returncode}\n")
            f.write(f"stdout: {stdout.decode('utf-8')}\n")
            f.write(f"stderr: {stderr.decode('utf-8')}\n")

        return result
