from __future__ import annotations

import os
import sys
import platform
import subprocess
import datetime
from pathlib import Path
from typing import Any, Dict, Optional

try:
    from shlex import join as shlex_join  # type: ignore[attr-defined]
except Exception:
    shlex_join = None  # type: ignore[assignment]


class ScriptRunner:
    '''Script executor, supports executing Python and Bash scripts'''

    def __init__(self, log_path: str = 'data/local_logs/train.log'):
        '''
        Initialize script executor
        Args:
            log_path: Base path for log files
        '''
        self.base_log_path = Path(log_path)
        self.base_log_dir = self.base_log_path.parent
        self.base_log_dir.mkdir(parents=True, exist_ok=True)
        self._last_log_file: Optional[Path] = None
        self._last_process: Optional[subprocess.Popen] = None

    def _prepare_log_file(self, script_type: str) -> str:
        '''
        Prepare log file
        Args:
            script_type: Script type, used for log directory naming
        Returns:
            str: Complete path to the log file
        '''
        ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        subdir = self.base_log_dir / script_type
        subdir.mkdir(parents=True, exist_ok=True)
        stem = self.base_log_path.stem or 'script'
        log_file = subdir / f'{stem}_{ts}.log'
        self._last_log_file = log_file
        return str(log_file)

    def _check_execution_env(self) -> Dict[str, str]:
        '''
        Get current execution environment information, supporting docker or regular system environment
        Returns:
            Dict[str, str]: Dictionary containing environment type and detailed information
        '''
        env_type = 'system'
        container_id = ''
        container_engine = ''

        # Detect docker/container
        try:
            if Path('/.dockerenv').exists():
                env_type = 'docker'
                container_engine = 'docker'
            else:
                # Inspect cgroup for container hints
                cgroup_paths = ['/proc/self/cgroup', '/proc/1/cgroup']
                for cg in cgroup_paths:
                    p = Path(cg)
                    if not p.exists():
                        continue
                    for line in p.read_text(errors='ignore').splitlines():
                        if any(k in line for k in ('docker', 'kubepods', 'containerd', 'podman', 'libpod')):
                            env_type = 'docker'
                            if 'podman' in line or 'libpod' in line:
                                container_engine = 'podman'
                            elif 'containerd' in line:
                                container_engine = 'containerd'
                            else:
                                container_engine = 'docker'
                            parts = [
                                seg for seg in line.strip().split('/') if seg]
                            if parts:
                                container_id = parts[-1]
                            break
                    if env_type != 'system':
                        break
        except Exception:
            # Best-effort detection; ignore errors
            pass

        return {
            'type': env_type,
            'engine': container_engine,
            'container_id': container_id,
            'hostname': platform.node(),
            'platform': platform.platform(),
            'os': f'{platform.system()} {platform.release()}',
            'architecture': platform.machine(),
            'python': self._check_python_version(),
        }

    def _check_python_version(self) -> str:
        '''
        Get Python version information
        Returns:
            str: Python version information
        '''
        try:
            impl = platform.python_implementation()
            ver = platform.python_version()
            return f'{impl} {ver} ({sys.executable})'
        except Exception:
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
        script = Path(script_path)
        if not script.exists():
            raise FileNotFoundError(f'Script not found: {script_path}')

        extra_args = [str(a) for a in (args or [])]

        if is_python:
            cmd = [sys.executable, '-u', str(script)] + extra_args
        else:
            if os.name == 'nt':
                # On Windows, use cmd to execute scripts/batch files
                cmd = ['cmd', '/c', str(script)] + extra_args
            else:
                # On POSIX, execute directly if executable; otherwise use sh
                if os.access(str(script), os.X_OK):
                    cmd = [str(script)] + extra_args
                else:
                    sh = '/bin/sh' if Path('/bin/sh').exists() else 'sh'
                    cmd = [sh, str(script)] + extra_args

        log_file_path = self._prepare_log_file(script_type)
        env_info = self._check_execution_env()
        started_at = datetime.datetime.utcnow().isoformat() + 'Z'

        # Write a header to the log file
        header_lines = [
            f'[{started_at}] Starting script',
            f'Command: {(shlex_join(cmd) if shlex_join else " ".join(cmd))}',
            f'Environment: type={env_info.get("type")} engine={env_info.get("engine")} hostname={env_info.get("hostname")}',
            f'Python: {env_info.get("python")}',
            '-' * 80,
        ]
        log_fh = open(log_file_path, 'a', encoding='utf-8', buffering=1)
        try:
            log_fh.write('\n'.join(header_lines) + '\n')
        except Exception:
            pass  # proceed even if header write fails

        proc = subprocess.Popen(
            cmd,
            stdout=log_fh,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            close_fds=os.name != 'nt',
        )

        self._last_process = proc

        result: Dict[str, Any] = {
            'pid': proc.pid,
            'env': env_info,
            'log_file': log_file_path,
            'cmd': cmd,
            'started_at': started_at,
            'returncode': None,
        }
        return result
