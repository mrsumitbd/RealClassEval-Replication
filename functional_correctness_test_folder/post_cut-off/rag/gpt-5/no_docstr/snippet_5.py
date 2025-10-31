from typing import Any, Dict, Optional
import os
import sys
import platform
import subprocess
import datetime
import shutil
import re


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
        # sanitize script_type for directory name
        safe_type = re.sub(r'[^A-Za-z0-9_\-\.]', '_', script_type or 'default')

        base_dir = os.path.dirname(self.base_log_path) or '.'
        base_name = os.path.splitext(os.path.basename(self.base_log_path))[
            0] or 'script'
        log_dir = os.path.join(base_dir, safe_type)
        os.makedirs(log_dir, exist_ok=True)

        ts = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        log_filename = f'{base_name}_{ts}.log'
        return os.path.join(log_dir, log_filename)

    def _check_execution_env(self) -> Dict[str, str]:
        '''
        Get current execution environment information, supporting docker or regular system environment
        Returns:
            Dict[str, str]: Dictionary containing environment type and detailed information
        '''
        env_type = 'system'
        detail = platform.platform()

        try:
            if os.path.exists('/.dockerenv'):
                env_type = 'docker'
            else:
                cgroup_path = '/proc/1/cgroup'
                if os.path.exists(cgroup_path):
                    with open(cgroup_path, 'r', encoding='utf-8', errors='ignore') as f:
                        cg = f.read()
                    if 'docker' in cg or 'containerd' in cg or 'kubepods' in cg:
                        # try to distinguish k8s vs docker
                        if 'kubepods' in cg or os.getenv('KUBERNETES_SERVICE_HOST'):
                            env_type = 'kubernetes'
                        else:
                            env_type = 'docker'
            # Additional hint if running in WSL
            if 'microsoft' in platform.release().lower():
                detail += ' (WSL)'
        except Exception:
            pass

        return {'type': env_type, 'detail': detail}

    def _check_python_version(self) -> str:
        '''
        Get Python version information
        Returns:
            str: Python version information
        '''
        return f'{platform.python_implementation()} {platform.python_version()} ({sys.executable})'

    def execute_script(self, script_path: str, script_type: str, is_python: bool = False, args: Optional[list] = None) -> Dict[str, Any]:
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
        result: Dict[str, Any] = {
            'pid': None,
            'env': self._check_execution_env(),
            'python_version': self._check_python_version(),
            'log_file': None,
            'command': None,
            'started': datetime.datetime.now().isoformat(timespec='seconds'),
            'status': 'pending',
        }

        if not script_path or not os.path.exists(script_path):
            result['status'] = 'error'
            result['error'] = f'script not found: {script_path}'
            return result

        extra_args = args or []
        log_file = self._prepare_log_file(script_type)
        result['log_file'] = log_file

        if is_python:
            cmd = [sys.executable, script_path] + list(extra_args)
        else:
            if os.name == 'nt':
                # Use cmd on Windows
                cmd = ['cmd', '/c', script_path] + list(extra_args)
            else:
                bash = shutil.which('bash')
                if bash:
                    cmd = [bash, script_path] + list(extra_args)
                else:
                    # Fallback to executing directly (requires executable bit or shebang)
                    cmd = [script_path] + list(extra_args)

        result['command'] = cmd

        header = [
            '=== ScriptRunner Start ===',
            f'Time: {result["started"]}',
            f'Env: {result["env"]["type"]} | {result["env"]["detail"]}',
            f'Python: {result["python_version"]}',
            f'Command: {" ".join(str(x) for x in cmd)}',
            f'Log: {log_file}',
            '==========================',
            ''
        ]

        try:
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            with open(log_file, 'a', encoding='utf-8') as lf:
                lf.write('\n'.join(header) + '\n')
                lf.flush()
                proc = subprocess.Popen(
                    cmd,
                    stdout=lf,
                    stderr=lf,
                    stdin=subprocess.DEVNULL,
                    close_fds=(os.name != 'nt'),
                    cwd=os.path.dirname(os.path.abspath(script_path)) or None,
                    text=False
                )
            result['pid'] = proc.pid
            result['status'] = 'started'
        except Exception as exc:
            result['status'] = 'error'
            result['error'] = str(exc)

            try:
                with open(log_file, 'a', encoding='utf-8') as lf:
                    lf.write(f'Error starting process: {exc}\n')
            except Exception:
                pass

        return result
