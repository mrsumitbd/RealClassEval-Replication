from typing import Optional

import os
import json
import subprocess
import sys


class ShortcutsCommand:
    '''处理快捷键安装和管理的命令'''

    def __init__(self):
        '''初始化快捷键命令'''
        self.shortcuts_file = os.path.expanduser("~/.shortcuts.json")
        self.shortcuts = self._load_shortcuts()

    def _load_shortcuts(self):
        if os.path.exists(self.shortcuts_file):
            try:
                with open(self.shortcuts_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_shortcuts(self):
        try:
            with open(self.shortcuts_file, "w", encoding="utf-8") as f:
                json.dump(self.shortcuts, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存快捷键失败: {e}", file=sys.stderr)

    def run(self, shell: Optional[str] = None) -> int:
        '''
        安装并管理快捷键
        '''
        print("快捷键管理：")
        print("1. 查看所有快捷键")
        print("2. 添加快捷键")
        print("3. 删除快捷键")
        print("4. 退出")
        try:
            while True:
                choice = input("请选择操作(1-4): ").strip()
                if choice == "1":
                    self._print_result({"shortcuts": self.shortcuts})
                elif choice == "2":
                    name = input("请输入快捷键名称: ").strip()
                    command = input("请输入命令: ").strip()
                    if name and command:
                        self.shortcuts[name] = command
                        self._save_shortcuts()
                        self._print_result(
                            {"msg": f"添加快捷键 {name} 成功", "shortcuts": self.shortcuts})
                    else:
                        self._print_result({"error": "名称和命令不能为空"})
                elif choice == "3":
                    name = input("请输入要删除的快捷键名称: ").strip()
                    if name in self.shortcuts:
                        del self.shortcuts[name]
                        self._save_shortcuts()
                        self._print_result(
                            {"msg": f"删除快捷键 {name} 成功", "shortcuts": self.shortcuts})
                    else:
                        self._print_result({"error": f"未找到快捷键 {name}"})
                elif choice == "4":
                    print("退出快捷键管理。")
                    return 0
                else:
                    print("无效选择，请重新输入。")
        except KeyboardInterrupt:
            print("\n已中断。")
            return 1
        except Exception as e:
            self._print_result({"error": str(e)})
            return 1

    def _print_result(self, result: dict) -> None:
        '''
        打印操作结果
        Args:
            result: 操作结果字典
        '''
        if "error" in result:
            print(f"错误: {result['error']}")
        elif "msg" in result:
            print(result["msg"])
        if "shortcuts" in result:
            print("当前快捷键列表：")
            for name, cmd in result["shortcuts"].items():
                print(f"  {name}: {cmd}")
