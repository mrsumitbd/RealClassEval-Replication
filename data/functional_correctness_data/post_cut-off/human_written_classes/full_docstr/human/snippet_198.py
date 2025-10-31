from viby.locale import get_text
from viby.utils.keyboard_shortcuts import install_shortcuts, detect_shell
from typing import Optional

class ShortcutsCommand:
    """处理快捷键安装和管理的命令"""

    def __init__(self):
        """初始化快捷键命令"""
        pass

    def run(self, shell: Optional[str]=None) -> int:
        """
        安装并管理快捷键
        """
        if not shell:
            detected_shell = detect_shell()
            if detected_shell:
                print(f"{get_text('SHORTCUTS', 'auto_detect_shell')}: {detected_shell}")
            else:
                print(get_text('SHORTCUTS', 'auto_detect_failed'))
            shell = detected_shell
        result = install_shortcuts(shell)
        self._print_result(result)
        return 0 if result.get('status') in ['success', 'info'] else 1

    def _print_result(self, result: dict) -> None:
        """
        打印操作结果

        Args:
            result: 操作结果字典
        """
        if result['status'] == 'success':
            status_color = '\x1b[92m'
        elif result['status'] == 'info':
            status_color = '\x1b[94m'
        else:
            status_color = '\x1b[91m'
        reset_color = '\x1b[0m'
        print(f"{status_color}[{result['status'].upper()}]{reset_color} {result['message']}")
        if 'action_required' in result:
            print(f"\n{get_text('SHORTCUTS', 'action_required').format(result['action_required'])}")
        if result['status'] == 'success':
            print(f"\n{get_text('SHORTCUTS', 'activation_note')}")