
from typing import Optional


class ShortcutsCommand:

    def __init__(self):
        '''初始化快捷键命令'''
        pass

    def run(self, shell: Optional[str] = None) -> int:
        '''
        安装并管理快捷键
        '''
        return 0

    def _print_result(self, result: dict) -> None:
        pass
