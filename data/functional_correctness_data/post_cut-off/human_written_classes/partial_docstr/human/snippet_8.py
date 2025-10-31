import subprocess
from typing import List, Optional, Dict, Any
import os
from lpm_kernel.common.logging import logger

class ScriptExecutor:

    def __init__(self):
        self.in_docker = os.getenv('IN_DOCKER_ENV') == '1' or os.path.exists('/.dockerenv')

    def execute(self, script_path: str, script_type: str, args: Optional[List[str]]=None, shell: bool=False, log_file: Optional[str]=None) -> Dict[str, Any]:
        """
        Execute scripts directly

        Args:
            script_path: Script path or command
            script_type: Script type, used for logging
            args: Command line arguments
            shell: Whether to use shell for execution
            log_file: Log file path, if provided will redirect output to this file

        Returns:
            Execution result
        """
        try:
            if script_path.endswith('.py'):
                cmd = ['python', '-u', script_path]
            elif script_path.endswith('.sh'):
                cmd = ['bash', '-x', script_path]
            else:
                cmd = [script_path]
            if args:
                cmd.extend(args)
            logger.info(f"Executing command: {' '.join(cmd)}")
            if log_file:
                os.makedirs(os.path.dirname(log_file), exist_ok=True)
            process = subprocess.Popen(cmd, shell=shell, env=os.environ.copy(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True)
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())
                    if log_file:
                        with open(log_file, 'a', encoding='utf-8') as f:
                            f.write(output)
            return_code = process.wait()
            if return_code != 0:
                logger.error(f'Command execution failed, return code: {return_code}')
            else:
                logger.info(f'Command execution successful, return code: {return_code}')
            return {'returncode': return_code, 'error': f'Execution failed, return code: {return_code}' if return_code != 0 else None}
        except Exception as e:
            error_msg = f'Error occurred while executing {script_type} script: {str(e)}'
            logger.error(error_msg)
            return {'error': error_msg, 'returncode': -1}