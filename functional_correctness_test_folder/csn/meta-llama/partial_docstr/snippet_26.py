
import subprocess


class System:

    @staticmethod
    def exec_command(command, getOutput=True):
        if getOutput:
            return subprocess.check_output(command, shell=True).decode('utf-8').strip()
        else:
            subprocess.run(command, shell=True)

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
