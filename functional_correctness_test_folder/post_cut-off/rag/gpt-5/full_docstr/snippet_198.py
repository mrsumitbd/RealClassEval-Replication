from typing import Optional, Dict
from pathlib import Path
import os
import platform
import re
from datetime import datetime


class ShortcutsCommand:
    """处理快捷键安装和管理的命令"""

    def __init__(self):
        """初始化快捷键命令"""
        self.marker_start = "# >>> shortcuts-command start >>>"
        self.marker_end = "# <<< shortcuts-command end <<<"
        self.default_aliases = {
            "ll": "ls -alF",
            "la": "ls -A",
            "l": "ls -CF",
            "gs": "git status -sb",
            "ga": "git add -A",
            "gc": "git commit",
            "gp": "git push",
            "gl": "git pull --rebase --autostash",
            "gd": "git diff",
            "gb": "git branch -vv",
            "gco": "git checkout",
        }

    def run(self, shell: Optional[str] = None) -> int:
        """
        安装并管理快捷键
        """
        result: Dict[str, object] = {
            "success": False,
            "shell": None,
            "profile": None,
            "updated": False,
            "message": "",
            "error": None,
        }
        try:
            shell_name = self._detect_shell(shell)
            if not shell_name:
                result["error"] = "无法检测到要配置的 shell，请指定 shell 参数（例如：bash/zsh/fish/powershell）"
                self._print_result(result)
                return 1
            result["shell"] = shell_name

            profile_path = self._get_profile_path(shell_name)
            result["profile"] = str(profile_path)

            block_text = self._generate_block(shell_name)

            updated = self._ensure_profile_block(profile_path, block_text)
            result["updated"] = updated
            result["success"] = True
            if updated:
                result["message"] = f"已将快捷键写入到 {profile_path}，重启或重新加载 shell 后生效。"
            else:
                result["message"] = f"{profile_path} 已包含最新快捷键配置，无需变更。"

        except Exception as exc:
            result["error"] = f"安装快捷键失败: {exc}"
            result["success"] = False

        self._print_result(result)
        return 0 if result.get("success") else 1

    def _print_result(self, result: dict) -> None:
        """
        打印操作结果
        Args:
            result: 操作结果字典
        """
        if result.get("success"):
            print("状态: 成功")
        else:
            print("状态: 失败")

        if result.get("shell"):
            print(f"Shell: {result['shell']}")

        if result.get("profile"):
            print(f"配置文件: {result['profile']}")

        if "updated" in result:
            print(f"是否修改: {'是' if result['updated'] else '否'}")

        if result.get("message"):
            print(f"消息: {result['message']}")

        if result.get("error"):
            print(f"错误: {result['error']}")

    def _detect_shell(self, shell: Optional[str]) -> Optional[str]:
        if shell:
            s = shell.strip().lower()
            if s in {"bash", "zsh", "fish", "powershell", "pwsh", "ps"}:
                return "powershell" if s in {"pwsh", "ps"} else s
            return None

        system = platform.system().lower()
        if system == "windows":
            return "powershell"

        env_shell = os.environ.get("SHELL", "")
        name = Path(env_shell).name.lower()
        if name in {"bash", "zsh", "fish"}:
            return name

        return None

    def _get_profile_path(self, shell_name: str) -> Path:
        home = Path.home()

        if shell_name == "bash":
            # 优先 .bashrc
            return home / ".bashrc"

        if shell_name == "zsh":
            return home / ".zshrc"

        if shell_name == "fish":
            return home / ".config" / "fish" / "config.fish"

        if shell_name == "powershell":
            docs = home / "Documents"
            ps7 = docs / "PowerShell" / "Microsoft.PowerShell_profile.ps1"
            ps5 = docs / "WindowsPowerShell" / "Microsoft.PowerShell_profile.ps1"
            if ps7.exists():
                return ps7
            if ps5.exists():
                return ps5
            return ps7

        # fallback
        return home / ".profile"

    def _generate_block(self, shell_name: str) -> str:
        if shell_name in {"bash", "zsh"}:
            lines = [self.marker_start]
            for name, cmd in self.default_aliases.items():
                lines.append(f"alias {name}='{cmd}'")
            lines.append(self.marker_end)
            return "\n".join(lines) + "\n"

        if shell_name == "fish":
            lines = [self.marker_start]
            for name, cmd in self.default_aliases.items():
                lines.append(f"function {name}")
                lines.append(f"    {cmd} $argv")
                lines.append("end")
            lines.append(self.marker_end)
            return "\n".join(lines) + "\n"

        if shell_name == "powershell":
            git_aliases = {
                k: v
                for k, v in self.default_aliases.items()
                if k.startswith("g")
            }
            lines = [self.marker_start]
            for name, cmd in git_aliases.items():
                lines.append(f"function {name} {{ {cmd} @args }}")
            lines.append(self.marker_end)
            return "\n".join(lines) + "\n"

        lines = [self.marker_start, "# 未知 shell，未生成任何别名", self.marker_end]
        return "\n".join(lines) + "\n"

    def _ensure_profile_block(self, profile_path: Path, block_text: str) -> bool:
        profile_path.parent.mkdir(parents=True, exist_ok=True)
        content_before = ""
        if profile_path.exists():
            content_before = profile_path.read_text(
                encoding="utf-8", errors="ignore")

        new_content = self._merge_block(content_before, block_text)

        if new_content == content_before:
            return False

        if content_before:
            ts = datetime.now().strftime("%Y%m%d%H%M%S")
            backup = profile_path.with_suffix(
                profile_path.suffix + f".bak.{ts}")
            backup.write_text(content_before, encoding="utf-8")

        profile_path.write_text(new_content, encoding="utf-8")
        return True

    def _merge_block(self, content: str, block_text: str) -> str:
        start_re = re.escape(self.marker_start)
        end_re = re.escape(self.marker_end)
        pattern = re.compile(
            rf"{start_re}.*?{end_re}\n?",
            flags=re.DOTALL,
        )

        if self.marker_start in content and self.marker_end in content:
            merged = pattern.sub(block_text, content)
            return merged

        sep = "" if content.endswith("\n") or content == "" else "\n"
        return content + sep + block_text
