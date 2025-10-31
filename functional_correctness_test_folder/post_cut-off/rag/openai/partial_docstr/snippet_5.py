
import os
import sys
import subprocess
import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class ScriptRunner:
    '''Script executor, supports executing Python and Bash scripts'''

    def __init__(self, log_path: str = 'data/local_logs/train.log'):
        '''
        Initialize script executor
        Args:
            log_path: Base path for log files
        '''
        self.log_path = Path(log_path).expanduser().resolve()
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def _prepare_log_file(self, script_type: str) -> str:
        '''
        Prepare log file
        Args:
            script_type: Script type, used for log directory naming
        Returns:
            str: Complete path to the log file
        '''
        now = datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
        log_dir = self.log_path.parent / script_type
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / f'{script_type}_{now}.log'
        return str(log_file)

    def _check_execution_env(self) -> Dict[str, str]:
        '''
        Get current execution environment information, supporting docker or regular system environment
        Returns:
            Dict[str, str]: Dictionary containing environment type and detailed information
        '''
        env_info: Dict[str, str] = {}
        # Detect Docker
        in_docker = False
        if os.path.exists('/.dockerenv'):
            in_docker = True
        else:
            try:
                with open('/proc/self/cgroup', 'rt') as f:
                    for line in f:
                        if 'docker' in line or 'lxc' in line:
                            in_docker = True
                            break
            except Exception:
                pass
        env_info['type'] = 'docker' if in_docker else 'system'
        # Add some details
        env_info['python_version'] = self._check_python_version()
        env_info['cwd'] = os.getcwd()
        env_info['env_vars'] = dict(os.environ)
        return env_info

    def _check_python_version(self) -> str:
        '''
        Get Python version information
        Returns:
            str: Python version information
        '''
        return sys.version.replace('\n', ' ')

    def execute_script(
        self,
        script_path: str,
        script_type: str,
        is_python: bool = False,
        args: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
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
        script_path = Path(script_path).expanduser().resolve()
        if not script_path.exists():
            raise FileNotFoundError(f'Script not found: {script_path}')

        log_file = self._prepare_log_file(script_type)
        env_info = self._check_execution_env()

        # Build command
        cmd: List[str] = []
        if is_python:
            cmd.append(sys.executable)
            cmd.append(str(script_path))
        else:
            cmd.append('/bin/bash')
            cmd.append(str(script_path))

        if args:
            cmd.extend(args)

        # Execute
        with open(log_file, 'w', encoding='utf-8') as lf:
            process = subprocess.Popen(
                cmd,
                stdout=lf,
                stderr=subprocess.STDOUT,
                env=os.environ,
            )
            pid = process.pid
            process.communicate()

        result: Dict[str, Any] = {
            'pid': pid,
            'env': env_info,
            'log_file': log_file,
            'exit_code': process.returncode,
        }
        return result
