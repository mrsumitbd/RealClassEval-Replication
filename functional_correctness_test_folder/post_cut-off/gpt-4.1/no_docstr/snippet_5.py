
import os
import sys
import subprocess
from typing import Dict, Any, Optional
import datetime


class ScriptRunner:

    def __init__(self, log_path: str = 'data/local_logs/train.log'):
        self.log_path = log_path
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)

    def _prepare_log_file(self, script_type: str) -> str:
        base, ext = os.path.splitext(self.log_path)
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = f"{base}_{script_type}_{timestamp}{ext}"
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        return log_file

    def _check_execution_env(self) -> Dict[str, str]:
        env_info = {
            'os': os.name,
            'platform': sys.platform,
            'cwd': os.getcwd(),
            'user': os.environ.get('USER') or os.environ.get('USERNAME', ''),
        }
        return env_info

    def _check_python_version(self) -> str:
        return sys.version

    def execute_script(self, script_path: str, script_type: str, is_python: bool = False, args: Optional[list] = None) -> Dict[str, Any]:
        log_file = self._prepare_log_file(script_type)
        cmd = []
        if is_python:
            cmd = [sys.executable, script_path]
        else:
            cmd = [script_path]
        if args:
            cmd += args

        result = {
            'returncode': None,
            'stdout': '',
            'stderr': '',
            'log_file': log_file,
            'env': self._check_execution_env(),
            'python_version': self._check_python_version(),
            'cmd': cmd
        }

        try:
            with open(log_file, 'w') as logf:
                proc = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )
                stdout, stderr = proc.communicate()
                logf.write(f"Command: {' '.join(cmd)}\n")
                logf.write(f"--- STDOUT ---\n{stdout}\n")
                logf.write(f"--- STDERR ---\n{stderr}\n")
                result['returncode'] = proc.returncode
                result['stdout'] = stdout
                result['stderr'] = stderr
        except Exception as e:
            result['stderr'] = str(e)
            result['returncode'] = -1
            with open(log_file, 'a') as logf:
                logf.write(f"Exception: {e}\n")
        return result
