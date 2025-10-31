
import subprocess


class System:

    @staticmethod
    def exec_command(command, getOutput=True):
        if getOutput:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True)
            return result.stdout, result.stderr, result.returncode
        else:
            subprocess.run(command, shell=True)
            return None, None, None

    @staticmethod
    def create_file(file_name, contents=''):
        with open(file_name, 'w') as file:
            file.write(contents)
