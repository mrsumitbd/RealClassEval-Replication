from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class ShortcutsCommand:
    '''处理快捷键安装和管理的命令'''

    START_MARK = "# >>> ShortcutsCommand >>>"
    END_MARK = "# <<< ShortcutsCommand <<<"

    def __init__(self):
        '''初始化快捷键命令'''
        # 通用快捷方式定义：名称 -> 命令
        # 注意：PowerShell 中带参数的别名需要用函数方式定义
        self.aliases: Dict[str, str] = {
            "gs": "git status -sb",
            "ga": "git add -A",
            "gc": "git commit -v",
            "gca": "git commit -v --amend",
            "gp": "git push",
            "gl": "git log --oneline --graph --decorate",
            "ll": "ls -alF",
            "la": "ls -A",
            "llh": "ls -alhF",
            "py": "python",
            "p3": "python3",
            "v": "vim",
        }

    def run(self, shell: Optional[str] = None) -> int:
        '''
        安装并管理快捷键
        '''
        result: Dict[str, object] = {
            "ok": False,
            "shell": None,
            "rc_file": None,
            "changed": False,
            "aliases": list(self.aliases.keys()),
            "action": "",
            "message": "",
        }
        try:
            sh = self._detect_shell(shell)
            if sh is None:
                result["message"] = "无法识别当前 shell，请通过 --shell 指定，例如：bash/zsh/fish/powershell"
                self._print_result(result)
                return 2

            rc_path = self._rc_path_for_shell(sh)
            if rc_path is None:
                result["shell"] = sh
                result["message"] = f"不支持的 shell：{sh}"
                self._print_result(result)
                return 2

            block = self._render_block_for_shell(sh)
            changed, action = self._ensure_block(rc_path, block)

            result.update({
                "ok": True,
                "shell": sh,
                "rc_file": str(rc_path),
                "changed": changed,
                "action": action,
                "message": "操作成功" if changed else "无需变更，已是最新",
            })
            self._print_result(result)
            return 0
        except Exception as exc:
            result["message"] = f"发生错误：{exc}"
            self._print_result(result)
            return 1

    def _print_result(self, result: dict) -> None:
        '''
        打印操作结果
        Args:
            result: 操作结果字典
        '''
        ok = result.get("ok", False)
        print("状态:", "成功" if ok else "失败")
        if result.get("shell"):
            print("Shell:", result["shell"])
        if result.get("rc_file"):
            print("配置文件:", result["rc_file"])
        if "changed" in result:
            print("是否有变更:", "是" if result["changed"] else "否")
        if "action" in result and result["action"]:
            print("操作:", result["action"])
        if "aliases" in result and result["aliases"]:
            print("快捷键数量:", len(result["aliases"]))
        if "message" in result and result["message"]:
            print("消息:", result["message"])

    # ---------------- 内部工具方法 ----------------

    def _detect_shell(self, shell: Optional[str]) -> Optional[str]:
        if shell:
            return self._normalize_shell_name(shell)

        # 优先从环境变量 SHELL (类 Unix)
        env_shell = os.environ.get("SHELL")
        if env_shell:
            return self._normalize_shell_name(Path(env_shell).name)

        # Windows 检测
        if os.name == "nt":
            # 判断 PowerShell
            if "PSModulePath" in os.environ or os.environ.get("TERM_PROGRAM") == "vscode":
                # VSCode 里可能多种 shell，这里优先当作 PowerShell
                return "powershell"
            comspec = os.environ.get("ComSpec", "").lower()
            if comspec.endswith("cmd.exe"):
                return "cmd"
            return "powershell"

        return None

    def _normalize_shell_name(self, name: str) -> Optional[str]:
        n = name.strip().lower()
        mapping = {
            "bash": "bash",
            "zsh": "zsh",
            "fish": "fish",
            "pwsh": "powershell",
            "powershell": "powershell",
            "ps": "powershell",
            "cmd": "cmd",
            "sh": "bash",
        }
        return mapping.get(n, None)

    def _rc_path_for_shell(self, shell: str) -> Optional[Path]:
        home = Path.home()

        if shell == "bash":
            return home / ".bashrc"
        if shell == "zsh":
            return home / ".zshrc"
        if shell == "fish":
            # 使用 config.fish，确保每次启动加载
            return home / ".config" / "fish" / "config.fish"
        if shell == "powershell":
            # 尝试 PowerShell 7+ 默认路径
            doc = home / "Documents"
            p1 = doc / "PowerShell" / "Microsoft.PowerShell_profile.ps1"
            p2 = doc / "WindowsPowerShell" / "Microsoft.PowerShell_profile.ps1"
            # 优先已有的
            if p1.exists():
                return p1
            if p2.exists():
                return p2
            # 不存在时优先创建 PowerShell 目录
            return p1
        if shell == "cmd":
            # cmd 没有统一的 profile 文件，暂不支持
            return None
        return None

    def _render_block_for_shell(self, shell: str) -> str:
        lines: List[str] = [self.START_MARK]
        if shell in ("bash", "zsh"):
            lines.append("# 安装由 ShortcutsCommand 管理的别名")
            for name, cmd in self.aliases.items():
                # 双引号包裹，转义内部引号
                safe_cmd = cmd.replace('"', r'\"')
                lines.append(f'alias {name}="{safe_cmd}"')
        elif shell == "fish":
            lines.append("# 安装由 ShortcutsCommand 管理的别名 (fish)")
            for name, cmd in self.aliases.items():
                # fish 支持 alias 内置命令（fish >= 3）
                safe_cmd = cmd.replace('"', r'\"')
                lines.append(f'alias {name} "{safe_cmd}"')
        elif shell == "powershell":
            lines.append("# 安装由 ShortcutsCommand 管理的别名/函数 (PowerShell)")
            for name, cmd in self.aliases.items():
                # PowerShell 中带参数的需要函数
                if " " in cmd or "-" in cmd:
                    # 使用函数包装，支持参数透传
                    # function name { <cmd> @Args }
                    lines.append(f"function {name} {{ {cmd} @Args }}")
                else:
                    # 简单命令可用 Set-Alias
                    lines.append(f"Set-Alias -Name {name} -Value {cmd}")
        else:
            # 不应发生：调用前已检查
            pass
        lines.append(self.END_MARK)
        # 统一以换行结束
        return "\n".join(lines) + "\n"

    def _ensure_block(self, rc_file: Path, block: str) -> Tuple[bool, str]:
        rc_file.parent.mkdir(parents=True, exist_ok=True)

        existing = ""
        if rc_file.exists():
            try:
                existing = rc_file.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                # 尝试 gbk（部分中文 Windows 环境）
                existing = rc_file.read_text(encoding="gbk", errors="ignore")

        # 正则移除所有旧块
        pattern = re.compile(
            rf"{re.escape(self.START_MARK)}.*?{re.escape(self.END_MARK)}\n?",
            re.DOTALL,
        )

        if existing:
            # 检查是否已有相同内容
            start_idx = existing.find(self.START_MARK)
            end_idx = existing.find(self.END_MARK)
            if start_idx != -1 and end_idx != -1:
                # 提取现有块，包含结束标记行
                end_idx = existing.find("\n", end_idx)
                if end_idx == -1:
                    end_idx = len(existing)
                current_block = existing[start_idx:end_idx]
                # 统一补全末尾换行以对齐比较
                if not current_block.endswith("\n"):
                    current_block += "\n"
                if current_block == block:
                    return (False, "no_change")

            cleaned = re.sub(pattern, "", existing).rstrip()
            new_content = (cleaned + "\n\n" + block) if cleaned else block
        else:
            new_content = block

        # 写回文件
        rc_file.write_text(new_content, encoding="utf-8")
        # 权限尽量友好（类 Unix）
        try:
            if os.name != "nt":
                rc_file.chmod(0o600)
        except Exception:
            pass

        # 判断是 install 还是 update
        action = "installed" if not existing else "updated"
        return (True, action)
