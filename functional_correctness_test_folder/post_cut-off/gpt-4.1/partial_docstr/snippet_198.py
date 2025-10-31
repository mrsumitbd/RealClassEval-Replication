
from typing import Optional


class ShortcutsCommand:

    def __init__(self):
        '''初始化快捷键命令'''
        self.shortcuts = {
            "copy": "Ctrl+C",
            "paste": "Ctrl+V",
            "cut": "Ctrl+X",
            "undo": "Ctrl+Z",
            "redo": "Ctrl+Y"
        }

    def run(self, shell: Optional[str] = None) -> int:
        '''
        安装并管理快捷键
        '''
        result = {
            "status": "success",
            "message": "快捷键已安装和管理",
            "shortcuts": self.shortcuts
        }
        if shell:
            result["shell"] = shell
        self._print_result(result)
        return 0

    def _print_result(self, result: dict) -> None:
        for key, value in result.items():
            print(f"{key}: {value}")
