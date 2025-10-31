
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
        获取指定shell的配置文件路径
        '''
        home_dir = os.path.expanduser('~')
        if shell == 'bash':
            config_file = os.path.join(home_dir, '.bashrc')
        elif shell == 'zsh':
            config_file = os.path.join(home_dir, '.zshrc')
        else:
            return None

        if os.path.exists(config_file):
            return config_file
        else:
            return None

    def _install_shortcuts(self, config_file: str, shell: str) -> dict:
        '''
        安装快捷键到指定的配置文件
        '''
        try:
            with open(config_file, 'r') as f:
                content = f.read()

            shortcut_code = f'''
# Added by ShortcutsCommand
alias ll="ls -l"
alias ..="cd .."
'''
            if shortcut_code.strip() not in content:
                with open(config_file, 'a') as f:
                    f.write(shortcut_code)

            subprocess.run([shell, '-c', f'source {config_file}'], check=True)
            return {'success': True, 'message': f'Shortcuts installed successfully for {shell}.'}
        except Exception as e:
            return {'success': False, 'message': f'Failed to install shortcuts for {shell}: {str(e)}'}

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
