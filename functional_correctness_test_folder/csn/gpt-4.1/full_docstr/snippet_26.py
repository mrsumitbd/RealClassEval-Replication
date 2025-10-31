
import subprocess


class System:
    '''
    Simplified access to some system commands.
    '''
    @staticmethod
    def exec_command(command, getOutput=True):
        '''
        Execute a shell command
        Usage: C{system.exec_command(command, getOutput=True)}
        Set getOutput to False if the command does not exit and return immediately. Otherwise
        AutoKey will not respond to any hotkeys/abbreviations etc until the process started
        by the command exits.
        @param command: command to be executed (including any arguments) - e.g. "ls -l"
        @param getOutput: whether to capture the (stdout) output of the command
        @raise subprocess.CalledProcessError: if the command returns a non-zero exit code
        '''
        if getOutput:
            result = subprocess.run(command, shell=True, check=True,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return result.stdout
        else:
            # Don't wait for output, just start the process
            process = subprocess.Popen(command, shell=True)
            return process

    @staticmethod
    def create_file(file_name, contents=''):
        '''
        Create a file with contents
        Usage: C{system.create_file(fileName, contents="")}
        @param fileName: full path to the file to be created
        @param contents: contents to insert into the file
        '''
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(contents)
