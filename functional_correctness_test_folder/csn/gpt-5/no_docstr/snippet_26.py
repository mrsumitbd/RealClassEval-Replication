
import os
import subprocess


class System:

    @staticmethod
    def exec_command(command, getOutput=True):
        try:
            use_shell = isinstance(command, str)
            result = subprocess.run(
                command,
                shell=use_shell,
                capture_output=True,
                text=True
            )
            if getOutput:
                return result.stdout.strip()
            return result.returncode
        except Exception:
            if getOutput:
                return ''
            return -1

    @staticmethod
    def create_file(file_name, contents=''):
        try:
            directory = os.path.dirname(os.path.abspath(file_name))
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(contents)
            return True
        except Exception:
            return False
