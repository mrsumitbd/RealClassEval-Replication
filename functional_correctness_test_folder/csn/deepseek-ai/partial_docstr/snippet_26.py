
import os
import subprocess


class System:

    @staticmethod
    def exec_command(command, getOutput=True):
        if getOutput:
            try:
                output = subprocess.check_output(
                    command, shell=True, stderr=subprocess.STDOUT)
                return output.decode('utf-8')
            except subprocess.CalledProcessError as e:
                return e.output.decode('utf-8')
        else:
            os.system(command)
            return None

    @staticmethod
    def create_file(file_name, contents=''):
        '''
        Create a file with contents
        Usage: C{system.create_file(fileName, contents="")}
        @param fileName: full path to the file to be created
        @param contents: contents to insert into the file
        '''
        with open(file_name, 'w') as f:
            f.write(contents)
