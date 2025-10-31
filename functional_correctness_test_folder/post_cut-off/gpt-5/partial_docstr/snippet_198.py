from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Optional, Tuple


class ShortcutsCommand:
    def __init__(self):
        '''初始化快捷键命令'''
        self.shortcuts = {
            "ll": "ls -alF",
            "la": "ls -A",
            "l": "ls -CF",
            "gs": "git status",
            "gd": "git diff",
            "gc": "git commit",
            "gp": "git push",
            "gl": "git log --oneline --graph --decorate",
            "gco": "git checkout",
            "gb": "git branch",
        }
        self.mark_start = "# >>> shortcuts start >>>"
        self.mark_end = "# <<< shortcuts end <<<"

    def run(self, shell: Optional[str] = None) -> int:
        '''
        安装并管理快捷键
        '''
        try:
            shell_name = self._detect_shell(shell)
            profile_path = self._profile_path_for_shell(shell_name)
            content = self._build_block(shell_name)

            profile_path.parent.mkdir(parents=True, exist_ok=True)
            updated = self._write_block(profile_path, content)

            result = {
                "shell": shell_name,
                "file": str(profile_path),
                "installed": sorted(self.shortcuts.keys()),
                "updated": updated,
            }
            self._print_result(result)
            return 0
        except Exception as e:
            sys.stderr.write(f"Error: {e}\n")
            return 1

    def _print_result(self, result: dict) -> None:
        print("快捷键安装完成")
        print(f"- Shell: {result.get('shell')}")
        print(f"- 配置文件: {result.get('file')}")
        print(f"- 已配置快捷键数量: {len(result.get('installed', []))}")
        print(f"- 是否更新: {'是' if result.get('updated') else '否'}")

    def _detect_shell(self, shell: Optional[str]) -> str:
        if shell:
            s = shell.strip().lower()
            s = Path(s).name  # handle full path like /bin/zsh
            if "zsh" in s:
                return "zsh"
            if "bash" in s:
                return "bash"
            if "fish" in s:
                return "fish"
            if "pwsh" in s or "powershell" in s or s == "ps":
                return "powershell"

        sh_env = os.environ.get("SHELL", "")
        if sh_env:
            base = Path(sh_env).name.lower()
            if "zsh" in base:
                return "zsh"
            if "bash" in base:
                return "bash"
            if "fish" in base:
                return "fish"

        if os.name == "nt":
            # Prefer PowerShell on Windows
            return "powershell"

        # Default to bash on POSIX
        return "bash"

    def _profile_path_for_shell(self, shell: str) -> Path:
        home = Path.home()
        shell = shell.lower()

        if shell == "zsh":
            return home / ".zshrc"
        if shell == "bash":
            # prefer .bashrc; macOS default interactive login shells may use .bash_profile
            return home / ".bashrc"
        if shell == "fish":
            return home / ".config" / "fish" / "config.fish"
        if shell == "powershell":
            # Try PowerShell 7 profile path first, then WindowsPowerShell
            docs = Path(os.environ.get("USERPROFILE", str(home))) / "Documents"
            pwsh_profile = docs / "PowerShell" / "Microsoft.PowerShell_profile.ps1"
            legacy_profile = docs / "WindowsPowerShell" / "Microsoft.PowerShell_profile.ps1"
            return pwsh_profile if pwsh_profile.exists() or not legacy_profile.exists() else legacy_profile

        # Fallback
        return home / ".profile"

    def _build_block(self, shell: str) -> str:
        if shell == "fish":
            body = self._build_fish_aliases()
        elif shell == "powershell":
            body = self._build_powershell_functions()
        else:
            body = self._build_sh_aliases()
        lines = [self.mark_start, body.rstrip(), self.mark_end, ""]
        return "\n".join(lines)

    def _build_sh_aliases(self) -> str:
        lines = ["# 自动生成的快捷键"]
        for k, v in sorted(self.shortcuts.items()):
            # Properly quote the command string
            cmd = v.replace("'", r"'\''")
            lines.append(f"alias {k}='{cmd}'")
        return "\n".join(lines)

    def _build_fish_aliases(self) -> str:
        lines = ["# 自动生成的快捷键 (fish)"]
        # fish alias builtin: alias name 'command ...'
        for k, v in sorted(self.shortcuts.items()):
            # Use single quotes around command to avoid expansions at definition time
            lines.append(f"alias {k} '{v}'")
        return "\n".join(lines)

    def _build_powershell_functions(self) -> str:
        lines = ["# 自动生成的快捷键 (PowerShell)"]
        # Use functions to support parameters; forward $args
        for k, v in sorted(self.shortcuts.items()):
            # Escape double quotes inside v
            cmd = v.replace("`", "``").replace('"', '\\"')
            lines.append(f"function {k} {{ {cmd} @args }}")
        return "\n".join(lines)

    def _write_block(self, path: Path, block: str) -> bool:
        if path.exists():
            current = path.read_text(encoding="utf-8", errors="ignore")
        else:
            current = ""

        start = self.mark_start
        end = self.mark_end

        if start in current and end in current:
            pre, _, rest = current.partition(start)
            _, _, post = rest.partition(end)
            new_content = pre.rstrip() + "\n" + block + post
            updated = new_content != current
        else:
            # Append at end
            sep = "" if current.endswith("\n") or not current else "\n\n"
            new_content = current + sep + block
            updated = True

        path.write_text(new_content, encoding="utf-8")
        return updated
