
import os
import sys
from typing import Optional, Dict


class ShortcutsCommand:
    '''处理快捷键安装和管理的命令'''

    def __init__(self):
        '''初始化快捷键命令'''
        # 这里可以初始化需要的属性，例如快捷键映射表
        self.shortcuts = {
            'ls': 'ls --color=auto',
            'll': 'ls -alF',
            'la': 'ls -A',
        }

    def run(self, shell: Optional[str] = None) -> int:
        '''
        安装并管理快捷键
        '''
        # 1. 确定使用的 shell
        if shell is None:
            shell = os.getenv('SHELL', '/bin/bash')
        shell_name = os.path.basename(shell)

        # 2. 执行安装逻辑
        result = self._install_shortcuts(shell_name)

        # 3. 打印结果
        self._print_result(result)

        # 4. 返回退出码
        return 0 if result.get('success', False) else 1

    def _install_shortcuts(self, shell_name: str) -> Dict[str, object]:
        '''
        根据 shell 类型安装快捷键
        '''
        # 仅支持 bash、zsh、fish
        supported = {'bash', 'zsh', 'fish'}
        if shell_name not in supported:
            return {
                'success': False,
                'error': f'Unsupported shell: {shell_name}',
            }

        # 这里模拟安装过程，实际实现可能会写入配置文件
        try:
            # 例如在 ~/.{shell_name}rc 中添加 alias
            rc_path = os.path.expanduser(f'~/.{shell_name}rc')
            with open(rc_path, 'a', encoding='utf-8') as f:
                for alias, cmd in self.shortcuts.items():
                    f.write(f'alias {alias}="{cmd}"\n')
            return {
                'success': True,
                'shell': shell_name,
                'rc_path': rc_path,
                'installed_aliases': list(self.shortcuts.keys()),
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }

    def _print_result(self, result: Dict[str, object]) -> None:
        '''
        打印操作结果
        Args:
            result: 操作结果字典
        '''
        if not result:
            print('No result to display.')
            return

        if result.get('success'):
            print(
                f"[SUCCESS] Installed shortcuts for shell: {result.get('shell')}")
            print(f"RC file updated: {result.get('rc_path')}")
            print(
                f"Aliases added: {', '.join(result.get('installed_aliases', []))}")
        else:
            print("[ERROR] Failed to install shortcuts.")
            print(f"Reason: {result.get('error')}")
