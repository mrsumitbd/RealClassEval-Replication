
from typing import Optional


class ShortcutsCommand:
    '''处理快捷键安装和管理的命令'''

    def __init__(self):
        '''初始化快捷键命令'''
        self.results = {}

    def run(self, shell: Optional[str] = None) -> int:
        '''
        安装并管理快捷键
        '''
        # 模拟安装和管理快捷键的过程
        if shell:
            self.results['status'] = 'success'
            self.results['message'] = f'Shortcuts installed for {shell}'
        else:
            self.results['status'] = 'error'
            self.results['message'] = 'No shell specified'

        self._print_result(self.results)
        return 0 if self.results['status'] == 'success' else 1

    def _print_result(self, result: dict) -> None:
        '''
        打印操作结果
        Args:
            result: 操作结果字典
        '''
        print(f"Status: {result['status']}")
        print(f"Message: {result['message']}")
