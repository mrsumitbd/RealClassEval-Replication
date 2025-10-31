
from typing import Optional


class ShortcutsCommand:
    '''处理快捷键安装和管理的命令'''

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

        # 假设这里是安装快捷键的逻辑
        self.shortcuts[shell] = True
        result = {"status": "success", "shell": shell}
        self._print_result(result)
        return 0

    def _print_result(self, result: dict) -> None:
        '''
        打印操作结果
        Args:
            result: 操作结果字典
        '''
        if result["status"] == "success":
            print(f"Shortcut installed successfully for {result['shell']}.")
        else:
            print(
                f"Failed to install shortcut: {result.get('error', 'Unknown error')}")
