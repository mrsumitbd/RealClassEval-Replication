
import os
import subprocess
import sys
from typing import Dict, Any, Optional
import logging
import datetime


class ScriptRunner:

    def __init__(self, log_path: str = 'data/local_logs/train.log'):
        self.log_path = log_path

    def _prepare_log_file(self, script_type: str) -> str:
        log_dir = os.path.dirname(self.log_path)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file_name = f'{script_type}_{timestamp}.log'
        log_file_path = os.path.join(log_dir, log_file_name)
        return log_file_path

    def _check_execution_env(self) -> Dict[str, str]:
        env_info = {}
        if os.path.exists('/.dockerenv'):
            env_info['type'] = 'docker'
            env_info['info'] = 'Running inside a Docker container'
        else:
            env_info['type'] = 'system'
            env_info['info'] = f'Running on {sys.platform} system'
        return env_info

    def _check_python_version(self) -> str:
        return sys.version

    def execute_script(self, script_path: str, script_type: str, is_python: bool = False, args: Optional[list] = None) -> Dict[str, Any]:
        log_file_path = self._prepare_log_file(script_type)
        env_info = self._check_execution_env()
        python_version = self._check_python_version()

        execution_result = {'log_path': log_file_path,
                            'env_info': env_info, 'python_version': python_version}

        try:
            with open(log_file_path, 'w') as log_file:
                if is_python:
                    command = [sys.executable, script_path]
                else:
                    command = [script_path]
                if args:
                    command.extend(args)
                subprocess.run(command, stdout=log_file,
                               stderr=log_file, check=True)
            execution_result['status'] = 'success'
        except subprocess.CalledProcessError as e:
            execution_result['status'] = 'failed'
            execution_result['error'] = str(e)
        except Exception as e:
            execution_result['status'] = 'failed'
            execution_result['error'] = str(e)

        return execution_result
