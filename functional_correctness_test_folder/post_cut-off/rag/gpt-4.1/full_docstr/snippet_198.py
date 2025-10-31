from typing import Optional

import os
import json
import sys
import shutil
import platform
import subprocess


class ShortcutsCommand:
    '''处理快捷键安装和管理的命令'''

    def __init__(self):
        '''初始化快捷键命令'''
        self.shortcuts = [
            {
                "name": "ll",
                "command": "ls -alF",
                "desc": "列出详细文件列表"
            },
            {
                "name": "gs",
                "command": "git status",
                "desc": "显示git状态"
            },
            {
                "name": "gco",
                "command": "git checkout",
                "desc": "切换分支"
            },
        ]
        self.supported_shells = ['bash', 'zsh']

    def run(self, shell: Optional[str] = None) -> int:
        '''
        安装并管理快捷键
        '''
        try:
            user_shell = shell or os.environ.get('SHELL', '')
            shell_name = os.path.basename(user_shell)
            if shell_name not in self.supported_shells:
                self._print_result({
                    "success": False,
                    "msg": f"暂不支持 {shell_name}，仅支持: {', '.join(self.supported_shells)}"
                })
                return 1

            home = os.path.expanduser('~')
            rcfile = os.path.join(home, f'.{shell_name}rc')
            if not os.path.exists(rcfile):
                with open(rcfile, 'w', encoding='utf-8') as f:
                    f.write('\n')

            with open(rcfile, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            new_aliases = []
            for shortcut in self.shortcuts:
                alias_line = f"alias {shortcut['name']}='{shortcut['command']}'\n"
                if not any(line.strip().startswith(f"alias {shortcut['name']}=") for line in lines):
                    new_aliases.append(alias_line)
                    lines.append(alias_line)

            if new_aliases:
                with open(rcfile, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                msg = f"已成功为 {shell_name} 安装 {len(new_aliases)} 个快捷键。请重新打开终端或执行 'source {rcfile}' 以生效。"
                self._print_result({"success": True, "msg": msg, "added": [
                                   a.strip() for a in new_aliases]})
                return 0
            else:
                self._print_result(
                    {"success": True, "msg": "所有快捷键已存在，无需重复安装。"})
                return 0
        except Exception as e:
            self._print_result({"success": False, "msg": f"安装快捷键时发生错误: {e}"})
            return 2

    def _print_result(self, result: dict) -> None:
        '''
        打印操作结果
        Args:
            result: 操作结果字典
        '''
        print(json.dumps(result, ensure_ascii=False, indent=2))
