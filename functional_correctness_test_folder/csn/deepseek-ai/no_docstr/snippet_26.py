
import subprocess
import os


class System:

    @staticmethod
    def exec_command(command, getOutput=True):
        try:
            if getOutput:
                result = subprocess.run(command, shell=True, check=True,
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        text=True)
                return result.stdout
            else:
                subprocess.run(command, shell=True, check=True)
                return None
        except subprocess.CalledProcessError as e:
            return e.stderr

    @staticmethod
    def create_file(file_name, contents=''):
        try:
            with open(file_name, 'w') as file:
                file.write(contents)
            return True
        except IOError:
            return False
