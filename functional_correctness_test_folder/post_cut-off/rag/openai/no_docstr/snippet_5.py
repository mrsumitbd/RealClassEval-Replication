
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
        self.base_log_path = Path(log_path).expanduser().resolve()
        self.base_log_path.parent.mkdir(parents=True, exist_ok=True)

    def _prepare_log_file(self, script_type: str) -> str:
        '''
        Prepare log file
        Args:
            script_type: Script type, used for log directory naming
        Returns:
            str: Complete path to the log file
        '''
        now = datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        log_dir = self.base_log_path.parent / script_type
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / f'{now}.log'
        return str(log_file)

    def _check_execution_env(self) -> Dict[str, str]:
        '''
        Get current execution environment information, supporting docker or regular system environment
        Returns:
            Dict[str, str]: Dictionary containing environment type and detailed information
        '''
        env_info: Dict[str, str] = {}
        # Detect docker
        in_docker = False
        if Path('/.dockerenv').exists():
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
        env_info['env_type'] = 'docker' if in_docker else 'system'
        # Add some system details
        try:
            uname = os.uname()
            env_info['details'] = f'{uname.sysname} {uname.release} {uname.machine}'
        except Exception:
            env_info['details'] = 'unknown'
        return env_info

    def _check_python_version(self) -> str:
        '''
        Get Python version information
        Returns:
            str: Python version information
        '''
        return sys.version

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

        log_file_path = self._prepare_log_file(script_type)
        env_info = self._check_execution_env()
        python_version = self._check_python_version()

        # Build command
        cmd: List[str] = []
        if is_python:
            cmd.append(sys.executable)
            cmd.append(str(script_path))
        else:
            # Ensure script is executable
            if not os.access(script_path, os.X_OK):
                # Try to run with bash
                cmd.append('bash')
                cmd.append(str(script_path))
            else:
                cmd.append(str(script_path))

        if args:
            cmd.extend(args)

        # Open log file
        log_file = open(log_file_path, 'w', encoding='utf-8')

        # Start process
        process = subprocess.Popen(
            cmd,
            stdout=log_file,
            stderr=subprocess.STDOUT,
            env=os.environ.copy(),
        )

        result: Dict[str, Any] = {
            'pid': process.pid,
            'env': env_info,
            'log_path': log_file_path,
            'python_version': python_version,
            'command': cmd,
        }

        # Wait for completion
        process.wait()
        log_file.close()
        result['returncode'] = process.returncode

        return result
