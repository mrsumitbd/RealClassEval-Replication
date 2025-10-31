
import subprocess
import os


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
        # Use subprocess.run to execute the command
        # shell=True allows passing a single string command
        # text=True decodes bytes to str
        result = subprocess.run(
            command,
            shell=True,
            capture_output=getOutput,
            text=True,
            check=True
        )
        # If getOutput is True, return stdout; otherwise return None
        return result.stdout if getOutput else None

    @staticmethod
    def create_file(file_name, contents=''):
        '''
        Create a file with contents
        Usage: C{system.create_file(fileName, contents="")}
        @param fileName: full path to the file to be created
        @param contents: contents to insert into the file
        '''
        # Ensure the directory exists
        dir_name = os.path.dirname(file_name)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        # Write the contents to the file
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(contents)
