from typing import Optional
import os
import sys
from pathlib import Path


class ShortcutsCommand:
    '''处理快捷键安装和管理的命令'''

    BLOCK_START = "# >>> ShortcutsCommand start >>>"
    BLOCK_END = "# <<< ShortcutsCommand end <<<"

    def __init__(self):
        '''初始化快捷键命令'''
        self.home = Path.home()

    def run(self, shell: Optional[str] = None) -> int:
        '''
        安装并管理快捷键
        '''
        try:
            resolved_shell = self._resolve_shell(shell)
            if not resolved_shell:
                self._print_result({
                    "ok": False,
                    "reason": "无法识别的 shell",
                    "shell": shell or "",
                })
                return 1

            path = self._rc_path_for_shell(resolved_shell)
            if not path:
                self._print_result({
                    "ok": False,
                    "reason": "暂不支持的 shell",
                    "shell": resolved_shell,
                })
                return 1

            content = self._render_block(resolved_shell)
            updated = self._ensure_block(path, content)

            self._print_result({
                "ok": True,
                "shell": resolved_shell,
                "path": str(path),
                "updated": updated,
            })
            return 0
        except Exception as e:
            self._print_result({
                "ok": False,
                "reason": f"发生异常: {e}",
                "shell": shell or "",
            })
            return 2

    def _print_result(self, result: dict) -> None:
        '''
        打印操作结果
        Args:
            result: 操作结果字典
        '''
        ok = result.get("ok", False)
        if ok:
            shell = result.get("shell", "?")
            path = result.get("path", "")
            updated = result.get("updated", False)
            action = "已更新" if updated else "已存在且无需变更"
            print(f"[OK] {shell} 快捷键 {action}: {path}")
            if path and shell in ("bash", "zsh"):
                print("提示: 运行 `source {}` 或重新打开终端生效".format(path))
            elif path and shell == "fish":
                print("提示: 重新打开终端或运行 `source {}` 生效".format(path))
            elif path and shell == "powershell":
                print("提示: 重新打开 PowerShell 生效")
            elif path and shell == "cmd":
                print("提示: 重新打开 CMD 生效")
        else:
            reason = result.get("reason", "未知错误")
            shell = result.get("shell", "")
            print(f"[FAIL] 安装快捷键失败: {reason} (shell={shell})", file=sys.stderr)

    # -------------- 内部实现 --------------

    def _resolve_shell(self, shell_hint: Optional[str]) -> Optional[str]:
        if shell_hint:
            s = shell_hint.strip().lower()
            if s in ("bash", "zsh", "fish", "powershell", "pwsh", "cmd"):
                return "powershell" if s in ("powershell", "pwsh") else s
            # 允许传可执行路径
            base = os.path.basename(s)
            if base in ("bash", "zsh", "fish", "pwsh", "powershell", "cmd.exe", "cmd"):
                if base in ("pwsh", "powershell"):
                    return "powershell"
                if base in ("cmd.exe", "cmd"):
                    return "cmd"
                return base

        # 自动检测
        if os.name == "nt":
            # 尝试区分 PowerShell 与 CMD
            parent = os.environ.get("ComSpec", "").lower()
            if "cmd.exe" in parent:
                # 优先检测 PowerShell 变量
                if "PSModulePath" in os.environ or "WT_SESSION" in os.environ:
                    return "powershell"
                return "cmd"
            else:
                # 在 Windows 上如果通过 pwsh/powershell 启动通常会有这些变量
                if "PSModulePath" in os.environ:
                    return "powershell"
                return "cmd"
        else:
            sh = os.environ.get("SHELL", "").strip().lower()
            base = os.path.basename(sh)
            if base in ("bash", "zsh", "fish"):
                return base
            # 无 SHELL 时默认 bash
            return "bash"

    def _rc_path_for_shell(self, shell: str) -> Optional[Path]:
        if shell == "bash":
            # 优先使用 .bashrc
            return self.home / ".bashrc"
        if shell == "zsh":
            return self.home / ".zshrc"
        if shell == "fish":
            return self.home / ".config" / "fish" / "config.fish"
        if shell == "powershell":
            # 跨平台定位 PowerShell 配置
            docs = Path(os.environ.get("USERPROFILE")
                        or self.home) / "Documents"
            # PS 7+ 默认目录
            pwsh_profile = docs / "PowerShell" / "Microsoft.PowerShell_profile.ps1"
            # Windows PowerShell 5.1
            winps_profile = docs / "WindowsPowerShell" / "Microsoft.PowerShell_profile.ps1"
            # 优先使用新版目录
            return pwsh_profile if not winps_profile.exists() else winps_profile
        if shell == "cmd":
            # CMD 没有全局 rc，只能写入用户级别的 init 脚本，退而求其次写入一个批处理放在家目录
            return self.home / "cmd_shortcuts.bat"
        return None

    def _render_block(self, shell: str) -> str:
        if shell in ("bash", "zsh"):
            body = [
                "# 常用别名",
                "alias ll='ls -alF'",
                "alias la='ls -A'",
                "alias l='ls -CF'",
                "",
                "# Git 快捷命令",
                "alias gs='git status'",
                "alias ga='git add'",
                "alias gc='git commit'",
                "alias gp='git push'",
            ]
            return "\n".join([self.BLOCK_START, *body, self.BLOCK_END, ""])
        if shell == "fish":
            body = [
                "# 常用别名 (fish)",
                "function ll; command ls -alF $argv; end",
                "function la; command ls -A $argv; end",
                "function l;  command ls -CF $argv; end",
                "",
                "# Git 快捷命令 (fish)",
                "function gs; command git status $argv; end",
                "function ga; command git add $argv; end",
                "function gc; command git commit $argv; end",
                "function gp; command git push $argv; end",
            ]
            return "\n".join([self.BLOCK_START, *body, self.BLOCK_END, ""])
        if shell == "powershell":
            body = [
                "# 常用别名 (PowerShell)",
                "function ll { Get-ChildItem -Force }",
                "function la { Get-ChildItem -Force -Name }",
                "Set-Alias -Name l -Value Get-ChildItem",
                "",
                "# Git 快捷命令 (PowerShell)",
                "Set-Alias gs 'git status'",
                "Set-Alias ga 'git add'",
                "Set-Alias gc 'git commit'",
                "Set-Alias gp 'git push'",
            ]
            return "\n".join([self.BLOCK_START, *body, self.BLOCK_END, ""])
        if shell == "cmd":
            body = [
                "REM 常用别名 (CMD 通过 doskey 实现，仅对当前会话有效)",
                "doskey ll=dir /a",
                "doskey la=dir /a /b",
                "doskey l=dir",
                "",
                "REM Git 快捷命令",
                "doskey gs=git status $*",
                "doskey ga=git add $*",
                "doskey gc=git commit $*",
                "doskey gp=git push $*",
            ]
            return "\n".join([self.BLOCK_START, *body, self.BLOCK_END, ""])
        return ""

    def _ensure_block(self, rc_path: Path, block: str) -> bool:
        rc_path.parent.mkdir(parents=True, exist_ok=True)
        existing = ""
        if rc_path.exists():
            try:
                existing = rc_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                existing = rc_path.read_text(encoding="utf-8", errors="ignore")

        # 移除旧块
        start = existing.find(self.BLOCK_START)
        end = existing.find(self.BLOCK_END)
        new_content: str
        if start != -1 and end != -1 and end >= start:
            end += len(self.BLOCK_END)
            prefix = existing[:start].rstrip()
            suffix = existing[end:].lstrip("\n")
            if prefix:
                new_content = prefix + "\n\n" + block + suffix
            else:
                new_content = block + suffix
        else:
            if existing and not existing.endswith("\n"):
                existing += "\n"
            new_content = existing + \
                ("\n" if existing and not existing.endswith("\n") else "") + block

        updated = new_content != existing
        if updated:
            rc_path.write_text(new_content, encoding="utf-8")
        return updated
