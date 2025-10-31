
from typing import Optional
import subprocess
import sys


class ShortcutsCommand:

    def __init__(self):
        pass

    def run(self, shell: Optional[str] = None) -> int:
        command = shell if shell is not None else "shortcuts list"
        try:
            result = subprocess.run(
                command,
                shell=True,
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            output = result.stdout.strip()
            error = result.stderr.strip()
            ret = result.returncode
            result_dict = {
                "command": command,
                "returncode": ret,
                "stdout": output,
                "stderr": error
            }
            self._print_result(result_dict)
            return ret
        except Exception as e:
            result_dict = {
                "command": command,
                "returncode": 1,
                "stdout": "",
                "stderr": str(e)
            }
            self._print_result(result_dict)
            return 1

    def _print_result(self, result: dict) -> None:
        print(f"Command: {result.get('command', '')}")
        print(f"Return code: {result.get('returncode', '')}")
        if result.get('stdout'):
            print("Output:")
            print(result['stdout'])
        if result.get('stderr'):
            print("Error:")
            print(result['stderr'], file=sys.stderr)
