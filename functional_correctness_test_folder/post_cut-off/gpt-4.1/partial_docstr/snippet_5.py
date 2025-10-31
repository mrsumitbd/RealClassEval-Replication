
import os
import sys
import subprocess
import platform
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
        env_info = {}
        # Check for Docker
        is_docker = False
        try:
            # Check /.dockerenv
            if os.path.exists('/.dockerenv'):
                is_docker = True
            else:
                # Check cgroup for docker
                with open('/proc/1/cgroup', 'rt') as f:
                    content = f.read()
                    if 'docker' in content or 'kubepods' in content:
                        is_docker = True
        except Exception:
            pass
        if is_docker:
            env_info['env_type'] = 'docker'
            env_info['details'] = 'Running inside a Docker container'
        else:
            env_info['env_type'] = 'system'
            env_info['details'] = platform.platform()
        return env_info

    def _check_python_version(self) -> str:
        return sys.version

    def execute_script(self, script_path: str, script_type: str, is_python: bool = False, args: Optional[list] = None) -> Dict[str, Any]:
        result = {
            'returncode': None,
            'stdout': '',
            'stderr': '',
            'log_file': '',
            'env_info': self._check_execution_env(),
            'python_version': self._check_python_version(),
        }
        log_file = self._prepare_log_file(script_type)
        result['log_file'] = log_file

        cmd = []
        if is_python:
            cmd = [sys.executable, script_path]
        else:
            cmd = [script_path]
        if args:
            cmd += args

        try:
            with open(log_file, 'w') as logf:
                proc = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )
                stdout, stderr = proc.communicate()
                logf.write('--- STDOUT ---\n')
                logf.write(stdout)
                logf.write('\n--- STDERR ---\n')
                logf.write(stderr)
                result['returncode'] = proc.returncode
                result['stdout'] = stdout
                result['stderr'] = stderr
        except Exception as e:
            result['stderr'] = str(e)
            result['returncode'] = -1
        return result
