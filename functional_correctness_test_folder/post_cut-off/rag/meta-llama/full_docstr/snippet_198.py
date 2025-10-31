
import os
import subprocess
from typing import Optional


class ShortcutsCommand:
    '''处理快捷键安装和管理的命令'''

    def __init__(self):
        '''初始化快捷键命令'''
        self.shortcuts_dir = os.path.join(
            os.path.expanduser('~'), '.local', 'share', 'applications')
        self.shortcuts_file = 'shortcut.desktop'

    def run(self, shell: Optional[str] = None) -> int:
        '''
        安装并管理快捷键
        '''
        if shell is None:
            shell = os.environ.get('SHELL', '/bin/bash').split('/')[-1]
        if shell not in ['bash', 'zsh']:
            print(f"Unsupported shell: {shell}")
            return 1

        result = self._install_shortcut(shell)
        self._print_result(result)
        return 0 if result['success'] else 1

    def _print_result(self, result: dict) -> None:
        '''
        打印操作结果
        Args:
            result: 操作结果字典
        '''
        if result['success']:
            print(f"Shortcut {result['action']} successfully.")
        else:
            print(
                f"Failed to {result['action']} shortcut: {result['message']}")

    def _install_shortcut(self, shell: str) -> dict:
        try:
            # Create shortcuts directory if not exists
            os.makedirs(self.shortcuts_dir, exist_ok=True)

            # Create shortcut file
            shortcut_path = os.path.join(
                self.shortcuts_dir, self.shortcuts_file)
            with open(shortcut_path, 'w') as f:
                f.write(
                    f"[Desktop Entry]\nName=Shortcut\nExec={os.path.abspath(__file__)}\nType=Application")

            # Make shortcut file executable
            subprocess.run(['chmod', '+x', shortcut_path])

            return {'success': True, 'action': 'installed', 'message': ''}
        except Exception as e:
            return {'success': False, 'action': 'install', 'message': str(e)}
