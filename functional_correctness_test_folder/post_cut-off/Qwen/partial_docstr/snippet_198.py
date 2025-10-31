
from typing import Optional


class ShortcutsCommand:

    def __init__(self):
        '''初始化快捷键命令'''
        self.shortcuts = {}

    def run(self, shell: Optional[str] = None) -> int:
        '''
        安装并管理快捷键
        '''
        if shell is None:
            shell = "default_shell"
        # Simulate installing or managing shortcuts
        self.shortcuts[shell] = "some_command"
        result = {"shell": shell, "status": "success",
                  "message": "Shortcut installed successfully"}
        self._print_result(result)
        return 0

    def _print_result(self, result: dict) -> None:
        print(
            f"Shell: {result['shell']}, Status: {result['status']}, Message: {result['message']}")
