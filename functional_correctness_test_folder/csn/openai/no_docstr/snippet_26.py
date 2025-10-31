
import os
import subprocess
from typing import Union


class System:
    @staticmethod
    def exec_command(command: str, getOutput: bool = True) -> Union[str, int]:
        """
        Execute a shell command.

        :param command: The command to run.
        :param getOutput: If True, return the command's stdout as a string.
                          If False, return the command's exit code.
        :return: stdout string if getOutput is True, otherwise the exit code.
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=getOutput,
                text=True,
                check=False,
            )
            if getOutput:
                # Combine stdout and stderr for easier debugging
                output = result.stdout
                if result.stderr:
                    output += "\n" + result.stderr
                return output.strip()
            else:
                return result.returncode
        except Exception as exc:
            # If an exception occurs, return the exception message
            return str(exc)

    @staticmethod
    def create_file(file_name: str, contents: str = "") -> None:
        """
        Create a file with the given contents. If the directory path does not exist,
        it will be created.

        :param file_name: Path to the file to create.
        :param contents: Text to write into the file.
        """
        dir_path = os.path.dirname(file_name)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(contents)
