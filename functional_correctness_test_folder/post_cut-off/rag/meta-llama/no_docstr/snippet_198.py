
import os
import subprocess
from typing import Optional


class ShortcutsCommand:
    '''处理快捷键安装和管理的命令'''

    def __init__(self):
        '''初始化快捷键命令'''
        self.supported_shells = ['bash', 'zsh']

    def run(self, shell: Optional[str] = None) -> int:
        '''
        安装并管理快捷键
        '''
        if shell is None:
            shell = os.path.basename(os.environ.get('SHELL', ''))
        if shell not in self.supported_shells:
            print(
                f"Unsupported shell: {shell}. Supported shells are: {', '.join(self.supported_shells)}")
            return 1

        config_file = self._get_config_file(shell)
        if not config_file:
            print(f"Failed to determine config file for {shell}.")
            return 1

        result = self._install_shortcuts(config_file, shell)
        self._print_result(result)
        return 0 if result['success'] else 1

    def _get_config_file(self, shell: str) -> Optional[str]:
        '''
        获取shell的配置文件路径
        '''
        home_dir = os.path.expanduser('~')
        if shell == 'bash':
            config_file = os.path.join(home_dir, '.bashrc')
        elif shell == 'zsh':
            config_file = os.path.join(home_dir, '.zshrc')
        else:
            return None

        if not os.path.exists(config_file):
            with open(config_file, 'w') as f:
                pass  # Create the file if it doesn't exist

        return config_file

    def _install_shortcuts(self, config_file: str, shell: str) -> dict:
        '''
        安装快捷键
        '''
        try:
            with open(config_file, 'r') as f:
                content = f.read()

            shortcut_code = f'\n# Added by ShortcutsCommand\nsource {os.path.dirname(__file__)}/shortcuts.{shell}\n'
            if shortcut_code.strip() in content:
                return {'success': True, 'message': 'Shortcuts are already installed.'}

            with open(config_file, 'a') as f:
                f.write(shortcut_code)

            return {'success': True, 'message': 'Shortcuts installed successfully.'}
        except Exception as e:
            return {'success': False, 'message': f'Failed to install shortcuts: {str(e)}'}

    def _print_result(self, result: dict) -> None:
        '''
        打印操作结果
        Args:
            result: 操作结果字典
        '''
        if result['success']:
            print(f"\033[92m{result['message']}\033[0m")
        else:
            print(f"\033[91m{result['message']}\033[0m")
