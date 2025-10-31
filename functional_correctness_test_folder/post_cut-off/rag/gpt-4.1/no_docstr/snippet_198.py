from typing import Optional

import os
import json
import subprocess
import sys


class ShortcutsCommand:
    '''处理快捷键安装和管理的命令'''

    def __init__(self):
        '''初始化快捷键命令'''
        self.shortcuts_file = os.path.expanduser('~/.shortcuts.json')
        self.shortcuts = self._load_shortcuts()

    def _load_shortcuts(self):
        if os.path.exists(self.shortcuts_file):
            try:
                with open(self.shortcuts_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_shortcuts(self):
        with open(self.shortcuts_file, 'w', encoding='utf-8') as f:
            json.dump(self.shortcuts, f, ensure_ascii=False, indent=2)

    def run(self, shell: Optional[str] = None) -> int:
        '''
        安装并管理快捷键
        '''
        print("快捷键管理：")
        print("1. 查看所有快捷键")
        print("2. 添加快捷键")
        print("3. 删除快捷键")
        print("4. 执行快捷键")
        print("5. 退出")
        while True:
            try:
                choice = input("请选择操作(1-5): ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return 0
            if choice == '1':
                self._print_result({'shortcuts': self.shortcuts})
            elif choice == '2':
                name = input("请输入快捷键名称: ").strip()
                if not name:
                    print("名称不能为空")
                    continue
                if name in self.shortcuts:
                    print("该快捷键已存在")
                    continue
                command = input("请输入命令: ").strip()
                if not command:
                    print("命令不能为空")
                    continue
                self.shortcuts[name] = command
                self._save_shortcuts()
                self._print_result(
                    {'add': name, 'command': command, 'status': 'success'})
            elif choice == '3':
                name = input("请输入要删除的快捷键名称: ").strip()
                if name in self.shortcuts:
                    del self.shortcuts[name]
                    self._save_shortcuts()
                    self._print_result({'delete': name, 'status': 'success'})
                else:
                    self._print_result({'delete': name, 'status': 'not found'})
            elif choice == '4':
                name = input("请输入要执行的快捷键名称: ").strip()
                if name in self.shortcuts:
                    command = self.shortcuts[name]
                    print(f"执行命令: {command}")
                    try:
                        if shell:
                            result = subprocess.run(
                                command, shell=True, executable=shell)
                        else:
                            result = subprocess.run(command, shell=True)
                        status = 'success' if result.returncode == 0 else f'failed({result.returncode})'
                        self._print_result(
                            {'run': name, 'command': command, 'status': status})
                    except Exception as e:
                        self._print_result(
                            {'run': name, 'command': command, 'status': f'error: {e}'})
                else:
                    self._print_result({'run': name, 'status': 'not found'})
            elif choice == '5':
                print("退出快捷键管理。")
                return 0
            else:
                print("无效选择，请重新输入。")

    def _print_result(self, result: dict) -> None:
        '''
        打印操作结果
        Args:
            result: 操作结果字典
        '''
        print(json.dumps(result, ensure_ascii=False, indent=2))
