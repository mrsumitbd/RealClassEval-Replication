
import os
import sys
import subprocess
import datetime
import uuid
from pathlib import Path
from typing import Dict, Any, Optional, List


class ScriptRunner:
    '''Script executor, supports executing Python and Bash scripts'''

    def __init__(self, log_path: str = 'data/local_logs/train.log'):
        '''
        Initialize script executor
        Args:
            log_path: Base path for log files
        '''
        self.log_path = Path(log_path).expanduser()
        # Ensure the base log directory exists
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def _prepare_log_file(self, script_type: str) -> str:
        '''
        Prepare log file
        Args:
            script_type: Script type, used for log directory naming
        Returns:
            str: Complete path to the log file
        '''
        # Create a subdirectory for the script type
        log_dir = self.log_path.parent / script_type
        log_dir.mkdir(parents=True, exist_ok=True)

        # Generate a unique log file name
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = uuid.uuid4().hex[:8]
        log_file = log_dir / f'{timestamp}_{unique_id}.log'
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
        # Common Docker indicators
        if Path('/.dockerenv').exists():
            in_docker = True
        else:
            try:
                with open('/proc/1/cgroup', 'r') as f:
                    for line in f:
                        if 'docker' in line or 'kubepods' in line:
                            in_docker = True
                            break
            except Exception:
                pass

        env_info['environment'] = 'docker' if in_docker else 'host'

        # Docker version if available
        if in_docker:
            try:
                result = subprocess.run(
                    ['docker', '--version'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    check=True
                )
                env_info['docker_version'] = result.stdout.strip()
            except Exception:
                env_info['docker_version'] = 'unknown'

        # Python version
        env_info['python_version'] = self._check_python_version()

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
        args: Optional[List[str]] = None
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
        if args is None:
            args = []

        # Resolve script path
        script_path = Path(script_path).expanduser()
        if not script_path.is_file():
            raise FileNotFoundError(f'Script not found: {script_path}')

        # Prepare log file
        log_file_path = self._prepare_log_file(script_type)

        # Build command
        if is_python:
            cmd = [sys.executable, str(script_path)] + args
        else:
            cmd = ['bash', str(script_path)] + args

        # Open log file for writing
        log_file = open(log_file_path, 'w', encoding='utf-8')

        # Start subprocess
        process = subprocess.Popen(
            cmd,
            stdout=log_file,
            stderr=subprocess.STDOUT,
            text=True,
            env=os.environ
        )

        # Gather execution info
        result: Dict[str, Any] = {
            'pid': process.pid,
            'log_file': log_file_path,
            'environment': self._check_execution_env(),
            'start_time': datetime.datetime.now().isoformat()
        }

        # Close log file handle (process will keep it open)
        log_file.close()

        return result
