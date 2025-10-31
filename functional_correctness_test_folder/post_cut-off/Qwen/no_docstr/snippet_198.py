
from typing import Optional


class ShortcutsCommand:

    def __init__(self):
        self.shortcuts = {
            'ls': 'List directory contents',
            'cd': 'Change directory',
            'pwd': 'Print working directory',
            'mkdir': 'Make directory',
            'rm': 'Remove file or directory',
            'cp': 'Copy file or directory',
            'mv': 'Move or rename file or directory',
            'touch': 'Create empty file',
            'cat': 'Concatenate and print files',
            'grep': 'Search text using patterns',
            'chmod': 'Change file mode bits',
            'chown': 'Change file owner and group',
            'ps': 'Report a snapshot of the current processes',
            'kill': 'Send a signal to a process',
            'top': 'Display processes',
            'df': 'Report file system disk space usage',
            'du': 'Estimate file space usage',
            'find': 'Search for files in a directory hierarchy',
            'tar': 'Archive files',
            'zip': 'Compress or extract files',
            'unzip': 'Extract files from a zip archive',
            'wget': 'Download files from the web',
            'curl': 'Transfer data with URLs',
            'man': 'Display manual pages',
            'history': 'Display command history',
            'exit': 'Exit the shell'
        }

    def run(self, shell: Optional[str] = None) -> int:
        if shell is None:
            shell = 'bash'
        result = {shell: self.shortcuts}
        self._print_result(result)
        return 0

    def _print_result(self, result: dict) -> None:
        for shell, commands in result.items():
            print(f"Shortcuts for {shell}:")
            for command, description in commands.items():
                print(f"  {command}: {description}")
