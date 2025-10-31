import os
import subprocess
from typing import Optional, Union


class System:
    '''
    Simplified access to some system commands.
    '''
    @staticmethod
    def exec_command(command: Union[str, list], getOutput: bool = True) -> Optional[str]:
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
            # Capture stdout (and stderr for richer exceptions), wait for completion, and raise on error
            completed = subprocess.run(
                command,
                shell=isinstance(command, str),
                text=True,
                capture_output=True,
                check=True,
            )
            return completed.stdout
        else:
            # Fire and forget: do not wait, do not capture output
            subprocess.Popen(
                command,
                shell=isinstance(command, str),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
                close_fds=True,
                start_new_session=True,
            )
            return None

    @staticmethod
    def create_file(file_name: str, contents: str = '') -> None:
        '''
        Create a file with contents
        Usage: C{system.create_file(fileName, contents="")}
        @param fileName: full path to the file to be created
        @param contents: contents to insert into the file
        '''
        dir_name = os.path.dirname(os.path.abspath(file_name))
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
        with open(file_name, 'w', encoding='utf-8', newline='') as f:
            f.write(contents)
