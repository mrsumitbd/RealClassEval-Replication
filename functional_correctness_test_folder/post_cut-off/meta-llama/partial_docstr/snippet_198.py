
from typing import Optional


class ShortcutsCommand:

    def __init__(self):
        '''初始化快捷键命令'''
        self.shortcuts = {}

    def run(self, shell: Optional[str] = None) -> int:
        '''
        安装并管理快捷键
        '''
        # 示例实现，实际逻辑根据需求修改
        if shell is None:
            print("Please specify a shell.")
            return 1

        # 假设这里是安装和管理快捷键的逻辑
        self.shortcuts[shell] = f"Shortcut for {shell} installed."

        self._print_result(self.shortcuts)
        return 0

    def _print_result(self, result: dict) -> None:
        '''打印结果'''
        for shell, message in result.items():
            print(f"{shell}: {message}")
