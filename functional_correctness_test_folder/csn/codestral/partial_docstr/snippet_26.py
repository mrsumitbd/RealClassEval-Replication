
import subprocess


class System:

    @staticmethod
    def exec_command(command, getOutput=True):
        if getOutput:
            result = subprocess.run(command, shell=True, check=True,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return result.stdout
        else:
            subprocess.run(command, shell=True, check=True)

    @staticmethod
    def create_file(file_name, contents=''):
        with open(file_name, 'w') as file:
            file.write(contents)
