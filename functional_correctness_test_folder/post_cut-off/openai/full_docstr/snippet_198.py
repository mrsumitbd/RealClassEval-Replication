
import os
import sys
import platform
from typing import Optional, Dict, Any


class ShortcutsCommand:
    '''处理快捷键安装和管理的命令'''

    def __init__(self):
        '''初始化快捷键命令'''
        self._os_name = platform.system()
        self._logger = self._get_logger()

    def _get_logger(self):
        # 简单的日志实现，实际项目可替换为更完整的日志框架
        class _Logger:
            def info(self, msg: str):
                print(f"[INFO] {msg}")

            def warning(self, msg: str):
                print(f"[WARN] {msg}")

            def error(self, msg: str):
                print(f"[ERROR] {msg}")

        return _Logger()

    def run(self, shell: Optional[str] = None) -> int:
        '''
        安装并管理快捷键
        '''
        # 1. 确定目标 shell
        if shell is None:
            if self._os_name == "Windows":
                shell = os.getenv("COMSPEC", "cmd.exe")
            else:
                shell = os.getenv("SHELL", "/bin/bash")

        # 2. 生成快捷键（这里仅做演示，实际实现会根据平台创建 .lnk 或 shell 脚本）
        try:
            shortcut_path = self._create_shortcut(shell)
            result = {
                "shell": shell,
                "shortcut_path": shortcut_path,
                "status": "success",
                "message": "快捷键已成功创建。",
            }
            self._logger.info(f"Shortcut created at {shortcut_path}")
            self._print_result(result)
            return 0
        except Exception as e:
            result = {
                "shell": shell,
                "status": "failure",
                "message": f"创建快捷键失败：{e}",
            }
            self._logger.error(result["message"])
            self._print_result(result)
            return 1

    def _create_shortcut(self, shell: str) -> str:
        """
        根据不同平台创建快捷键文件。
        这里只是一个演示实现，实际项目中需要根据需求创建真正的快捷方式。
        """
        if self._os_name == "Windows":
            # 在 Windows 上创建一个简单的 .lnk 文件（仅演示，实际需要 COM 接口）
            shortcut_name = os.path.basename(
                shell).replace(".exe", "") + ".lnk"
            shortcut_path = os.path.join(
                os.path.expanduser("~"), "Desktop", shortcut_name)
            with open(shortcut_path, "w", encoding="utf-8") as f:
                f.write(f"Shortcut to {shell}\n")
            return shortcut_path
        else:
            # 在类 Unix 系统上创建一个符号链接或 shell 脚本
            shortcut_name = os.path.basename(shell) + "_shortcut"
            shortcut_path = os.path.join(os.path.expanduser(
                "~"), ".local", "bin", shortcut_name)
            os.makedirs(os.path.dirname(shortcut_path), exist_ok=True)
            with open(shortcut_path, "w", encoding="utf-8") as f:
                f.write(f"#!/bin/sh\nexec {shell} \"$@\"\n")
            os.chmod(shortcut_path, 0o755)
            return shortcut_path

    def _print_result(self, result: Dict[str, Any]) -> None:
        '''
        打印操作结果
        Args:
            result: 操作结果字典
        '''
        print("\n=== 操作结果 ===")
        for key, value in result.items():
            print(f"{key}: {value}")
        print("=================\n")
