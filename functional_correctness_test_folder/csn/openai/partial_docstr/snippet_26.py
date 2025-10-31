
import subprocess
import os


class System:
    @staticmethod
    def exec_command(command, getOutput=True):
        """
        Execute a shell command.

        :param command: The command string to execute.
        :param getOutput: If True, return the command's stdout as a string.
                          If False, return the command's exit code.
        :return: stdout string or exit code.
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            if getOutput:
                return result.stdout
            else:
                return result.returncode
        except Exception as e:
            if getOutput:
                return str(e)
            else:
                return -1

    @staticmethod
    def create_file(file_name, contents=''):
        """
        Create a file with the specified contents.

        :param file_name: Full path to the file to be created.
        :param contents: String to write into the file.
        """
        # Ensure the directory exists
        dir_name = os.path.dirname(file_name)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)

        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(contents)
