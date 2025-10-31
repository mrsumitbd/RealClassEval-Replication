class System:

    @staticmethod
    def exec_command(command, getOutput=True):
        import subprocess
        import shlex

        try:
            if isinstance(command, (list, tuple)):
                cmd = list(command)
                shell = False
            else:
                cmd = command
                shell = True

            result = subprocess.run(
                cmd if shell else cmd,
                shell=shell,
                capture_output=getOutput,
                text=True
            )

            if getOutput:
                return (result.stdout, result.stderr, result.returncode)
            else:
                return result.returncode
        except Exception as e:
            if getOutput:
                return ("", str(e), -1)
            else:
                return -1

    @staticmethod
    def create_file(file_name, contents=''):
        '''
        Create a file with contents
        Usage: C{system.create_file(fileName, contents="")}
        @param fileName: full path to the file to be created
        @param contents: contents to insert into the file
        '''
        import os

        directory = os.path.dirname(os.path.abspath(file_name))
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(contents if contents is not None else '')

        return True
