
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
        # 示例：添加、删除、列出快捷键
        # 这里只做简单模拟
        result = {}
        if shell is None:
            # 默认列出所有快捷键
            result['action'] = 'list'
            result['shortcuts'] = self.shortcuts.copy()
            self._print_result(result)
            return 0
        else:
            # 假设shell为"add:name:command"或"remove:name"
            if shell.startswith("add:"):
                try:
                    _, name, command = shell.split(":", 2)
                    self.shortcuts[name] = command
                    result['action'] = 'add'
                    result['name'] = name
                    result['command'] = command
                    result['success'] = True
                except Exception:
                    result['action'] = 'add'
                    result['success'] = False
                self._print_result(result)
                return 0 if result.get('success') else 1
            elif shell.startswith("remove:"):
                try:
                    _, name = shell.split(":", 1)
                    if name in self.shortcuts:
                        del self.shortcuts[name]
                        result['action'] = 'remove'
                        result['name'] = name
                        result['success'] = True
                    else:
                        result['action'] = 'remove'
                        result['name'] = name
                        result['success'] = False
                except Exception:
                    result['action'] = 'remove'
                    result['success'] = False
                self._print_result(result)
                return 0 if result.get('success') else 1
            else:
                result['action'] = 'unknown'
                result['success'] = False
                self._print_result(result)
                return 1

    def _print_result(self, result: dict) -> None:
        '''
        打印操作结果
        Args:
            result: 操作结果字典
        '''
        action = result.get('action')
        if action == 'list':
            print("当前快捷键列表：")
            if not result['shortcuts']:
                print("  (无快捷键)")
            else:
                for name, command in result['shortcuts'].items():
                    print(f"  {name}: {command}")
        elif action == 'add':
            if result.get('success'):
                print(
                    f"已添加快捷键: {result.get('name')} -> {result.get('command')}")
            else:
                print("添加快捷键失败。")
        elif action == 'remove':
            if result.get('success'):
                print(f"已移除快捷键: {result.get('name')}")
            else:
                print("移除快捷键失败。")
        else:
            print("未知操作。")
