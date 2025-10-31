from typing import Dict, Any, Optional
import os
import sys
import json
import platform
import socket
import getpass
import datetime
import subprocess
from pathlib import Path


class ScriptRunner:
    '''Script executor, supports executing Python and Bash scripts'''

    def __init__(self, log_path: str = 'data/local_logs/train.log'):
        '''
        Initialize script executor
        Args:
            log_path: Base path for log files
        '''
        self.base_log_path = Path(log_path)

    def _prepare_log_file(self, script_type: str) -> str:
        '''
        Prepare log file
        Args:
            script_type: Script type, used for log directory naming
        Returns:
            str: Complete path to the log file
        '''
        # Use directory of base_log_path as base dir; place logs under script_type subdir
        base_dir = self.base_log_path.parent if self.base_log_path.parent != Path(
            '') else Path('.')
        log_dir = base_dir / script_type
        log_dir.mkdir(parents=True, exist_ok=True)

        base_name = self.base_log_path.stem or 'script'
        ts = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        log_file = log_dir / f'{base_name}_{script_type}_{ts}.log'
        return str(log_file.resolve())

    def _check_execution_env(self) -> Dict[str, str]:
        '''
        Get current execution environment information, supporting docker or regular system environment
        Returns:
            Dict[str, str]: Dictionary containing environment type and detailed information
        '''
        env_type = 'system'
        details = 'regular system environment'
        try:
            if Path('/.dockerenv').exists():
                env_type = 'docker'
                details = '/.dockerenv present'
            else:
                cgroup_path = Path('/proc/1/cgroup')
                if cgroup_path.exists():
                    content = cgroup_path.read_text(errors='ignore')
                    if any(x in content for x in ('docker', 'kubepods', 'containerd')):
                        env_type = 'docker'
                        details = 'cgroup indicates container (docker/kubepods/containerd)'
        except Exception as e:
            details = f'error detecting environment: {e}'

        info = {
            'env_type': env_type,
            'details': details,
            'platform': platform.platform(),
            'system': platform.system(),
            'machine': platform.machine(),
            'release': platform.release(),
            'version': platform.version(),
            'hostname': socket.gethostname(),
            'user': getpass.getuser(),
            'cwd': str(Path.cwd()),
        }
        return info

    def _check_python_version(self) -> str:
        '''
        Get Python version information
        Returns:
            str: Python version information
        '''
        return sys.version.replace('\n', ' ')

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
        args = args or []
        script_path = str(Path(script_path).expanduser().resolve())

        if is_python:
            cmd = [sys.executable, script_path] + [str(a) for a in args]
        else:
            if script_path.endswith('.sh'):
                cmd = ['bash', script_path] + [str(a) for a in args]
            else:
                cmd = [script_path] + [str(a) for a in args]

        log_file = self._prepare_log_file(script_type)
        env_info = self._check_execution_env()
        py_ver = self._check_python_version()
        started_at = datetime.datetime.now().isoformat(timespec='seconds')

        header = {
            'started_at': started_at,
            'command': cmd,
            'environment': env_info,
            'python_version': py_ver,
            'script_path': script_path,
            'script_type': script_type,
        }

        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write('=== Script Execution Started ===\n')
            f.write(json.dumps(header, ensure_ascii=False))
            f.write('\n=== Realtime Output ===\n')
            f.flush()

        # Launch process with stdout/stderr redirected to log
        logfile_handle = open(log_file, 'a', encoding='utf-8')
        try:
            proc = subprocess.Popen(
                cmd,
                stdout=logfile_handle,
                stderr=subprocess.STDOUT,
                cwd=env_info.get('cwd', None)
            )
        except Exception as e:
            logfile_handle.write(f'\n[ERROR] Failed to start process: {e}\n')
            logfile_handle.flush()
            logfile_handle.close()
            return {
                'pid': None,
                'started_at': started_at,
                'command': cmd,
                'log_file': log_file,
                'environment': env_info,
                'python_version': py_ver,
                'error': str(e),
            }

        # Do not wait; return immediately with PID and context
        result = {
            'pid': proc.pid,
            'started_at': started_at,
            'command': cmd,
            'log_file': log_file,
            'environment': env_info,
            'python_version': py_ver,
        }
        # We keep the file handle open for the child process; it will be closed when process exits.
        # No explicit close here to avoid truncating/closing while the child writes.
        return result
