
import subprocess
import os


class System:

    @staticmethod
    def exec_command(command, getOutput=True):
        if getOutput:
            result = subprocess.run(
                command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return result.stdout
        else:
            subprocess.run(command, shell=True)
            return None

    @staticmethod
    def create_file(file_name, contents=''):
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(contents)
