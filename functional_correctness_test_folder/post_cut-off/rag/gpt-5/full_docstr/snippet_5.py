from __future__ import annotations

import os
import platform
import re
import shutil
import socket
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional


@dataclass
class _Command:
    argv: list[str]
    shell: bool = False


class ScriptRunner:
    '''Script executor, supports executing Python and Bash scripts'''

    def __init__(self, log_path: str = 'data/local_logs/train.log'):
        '''
        Initialize script executor
        Args:
            log_path: Base path for log files
        '''
        base = Path(log_path).expanduser().resolve()
        # If a .log path is provided, use its parent as the base log directory.
        self.base_log_dir = base.parent if base.suffix.lower() == '.log' else base
        self.base_log_dir.mkdir(parents=True, exist_ok=True)

    def _prepare_log_file(self, script_type: str) -> str:
        '''
        Prepare log file
        Args:
            script_type: Script type, used for log directory naming
        Returns:
            str: Complete path to the log file
        '''
        stype = (script_type or 'default').strip()
        stype = re.sub(r'[^A-Za-z0-9_.-]+', '_', stype) or 'default'
        log_dir = self.base_log_dir / stype
        log_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')
        log_file = log_dir / f'{timestamp}-{os.getpid()}.log'
        # Touch file to ensure it exists and is writable
        log_file.touch(exist_ok=True)
        return str(log_file)

    def _check_execution_env(self) -> Dict[str, str]:
        '''
        Get current execution environment information, supporting docker or regular system environment
        Returns:
            Dict[str, str]: Dictionary containing environment type and detailed information
        '''
        env_type = 'host'
        is_docker = False
        is_k8s = False

        try:
            if Path('/.dockerenv').exists():
                is_docker = True
            else:
                cgroup = Path('/proc/1/cgroup')
                if cgroup.exists():
                    content = cgroup.read_text(
                        encoding='utf-8', errors='ignore')
                    if 'docker' in content or 'kubepods' in content or 'containerd' in content:
                        is_docker = True
        except Exception:
            pass

        if os.environ.get('KUBERNETES_SERVICE_HOST'):
            is_k8s = True

        if is_k8s:
            env_type = 'kubernetes'
        elif is_docker:
            env_type = 'docker'

        details: Dict[str, str] = {
            'type': env_type,
            'platform': platform.platform(),
            'system': platform.system(),
            'release': platform.release(),
            'machine': platform.machine(),
            'processor': platform.processor() or '',
            'hostname': socket.gethostname(),
            'user': os.environ.get('USER') or os.environ.get('USERNAME', ''),
            'cwd': os.getcwd(),
            'python': self._check_python_version(),
        }
        return {k: str(v) for k, v in details.items()}

    def _check_python_version(self) -> str:
        '''
        Get Python version information
        Returns:
            str: Python version information
        '''
        return f'{platform.python_version()} ({sys.executable})'

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
        result: Dict[str, Any] = {}
        args = [str(a) for a in (args or [])]
        script = Path(script_path).expanduser().resolve()

        if not script.exists():
            return {
                'success': False,
                'error': f'Script not found: {script}',
                'env': self._check_execution_env(),
            }

        log_file = self._prepare_log_file(script_type)
        env_info = self._check_execution_env()

        def build_command() -> _Command:
            if is_python or script.suffix.lower() == '.py':
                return _Command([sys.executable, str(script), *args])
            # Prefer bash/sh on POSIX
            if os.name != 'nt':
                sh = shutil.which('bash') or shutil.which('sh')
                if sh:
                    return _Command([sh, str(script), *args])
                # Fallback to executing directly if executable bit set
                if os.access(str(script), os.X_OK):
                    return _Command([str(script), *args])
                # Last resort: run via /bin/sh -c "script args"
                return _Command(['sh', str(script), *args])
            # Windows handling
            # If bash available on Windows (Git Bash/WSL), prefer it for .sh
            if script.suffix.lower() == '.sh':
                bash = shutil.which('bash')
                if bash:
                    return _Command([bash, str(script), *args])
            if script.suffix.lower() == '.ps1':
                pwsh = shutil.which('pwsh') or shutil.which('powershell')
                if pwsh:
                    return _Command([pwsh, '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', str(script), *args])
            cmd = shutil.which('cmd') or 'cmd'
            return _Command([cmd, '/c', str(script), *args])

        cmd = build_command()
        start = time.time()
        start_iso = datetime.now(timezone.utc).isoformat()
        try:
            with open(log_file, 'a', encoding='utf-8', errors='ignore') as fh:
                fh.write(f'=== ScriptRunner start {start_iso} ===\n')
                fh.write(f'Command: {" ".join(cmd.argv)}\n')
                fh.write(f'Environment: {env_info}\n')
                fh.flush()
                proc = subprocess.Popen(
                    cmd.argv,
                    stdout=fh,
                    stderr=subprocess.STDOUT,
                    shell=cmd.shell,
                    cwd=str(script.parent)
                )
                pid = proc.pid
                ret = proc.wait()
                end = time.time()
                end_iso = datetime.now(timezone.utc).isoformat()
                duration = end - start
                fh.write(
                    f'=== ScriptRunner end {end_iso} (rc={ret}, duration={duration:.3f}s) ===\n')
        except Exception as exc:
            end = time.time()
            return {
                'success': False,
                'error': str(exc),
                'env': env_info,
                'log_file': log_file,
                'start_time': start_iso,
                'end_time': datetime.now(timezone.utc).isoformat(),
                'duration_sec': end - start,
                'command': cmd.argv if 'cmd' in locals() else [],
            }

        result.update(
            {
                'success': ret == 0,
                'pid': pid,
                'returncode': ret,
                'env': env_info,
                'log_file': log_file,
                'command': cmd.argv,
                'start_time': start_iso,
                'end_time': datetime.now(timezone.utc).isoformat(),
                'duration_sec': end - start,
                'script_path': str(script),
                'script_type': script_type,
                'is_python': bool(is_python or script.suffix.lower() == '.py'),
            }
        )
        return result
