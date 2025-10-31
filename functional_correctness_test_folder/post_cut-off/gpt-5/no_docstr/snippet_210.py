from typing import Optional, List
import subprocess
import os
import shlex
import stat
from pathlib import Path


class Shell:

    def __init__(self, dry_run: bool = False, safe_mode: bool = True):
        self.dry_run = dry_run
        self.safe_mode = safe_mode

    def _validate_command_safety(self, cmd: str) -> None:
        if not self.safe_mode:
            return

        lowered = cmd.lower().strip()

        forbidden_substrings = [
            " shutdown", "shutdown ",
            " reboot", "reboot ",
            " poweroff", "poweroff ",
            " halt", "halt ",
            " mkfs", "mkfs.",
            " :(){:|:&};:",  # fork bomb
            " format ",
            "rm -rf /",
            "rm -rf --no-preserve-root /",
            "dd if=/dev/zero",
            " del /s ", " del /q ", " rmdir /s ",
        ]

        for bad in forbidden_substrings:
            if bad in f" {lowered} ":
                raise ValueError(
                    f"Unsafe command detected in safe_mode: {bad.strip()}")

        destructive_binaries = {
            "rm": ["-rf", "--no-preserve-root"],
            "dd": ["of=/dev/sd", "of=/dev/nvme", "of=/dev/mmcblk"],
            "chmod": ["-R 000", " -R 0 "],
            "chown": [" -R "],
        }

        try:
            tokens = shlex.split(cmd)
        except Exception:
            tokens = lowered.split()

        if tokens:
            exe = os.path.basename(tokens[0]).lower()
            args = " ".join(tokens[1:]).lower()
            if exe in destructive_binaries:
                for marker in destructive_binaries[exe]:
                    if marker in args:
                        raise ValueError(
                            f"Unsafe command detected in safe_mode: {exe} {marker}")

        critical_paths = ["/", "/bin", "/sbin", "/usr", "/etc",
                          "/lib", "/lib64", "/boot", "/dev", "/proc", "/sys"]
        for p in critical_paths:
            if f" {p} " in f" {lowered} ":
                # Only flag if combined with potentially destructive verbs
                dangerous_verbs = ["rm", "dd", "mkfs",
                                   "cp -r", "mv", "chmod -r", "chown -r"]
                for v in dangerous_verbs:
                    if lowered.startswith(v) or f" {v} " in lowered:
                        raise ValueError(
                            "Unsafe command involving critical system path in safe_mode")

    def run(self, *parts: str, timeout: int = 30, cwd: Optional[str] = None) -> str:
        if not parts:
            return ""
        cmd_list: List[str] = list(parts)
        cmd_str = " ".join(parts)
        self._validate_command_safety(cmd_str)

        if self.dry_run:
            return ""

        proc = subprocess.run(
            cmd_list,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=cwd,
            timeout=timeout,
            check=True,
        )
        return proc.stdout

    def run_check(self, *parts: str, timeout: int = 30, cwd: Optional[str] = None) -> bool:
        if not parts:
            return True
        cmd_list: List[str] = list(parts)
        cmd_str = " ".join(parts)
        self._validate_command_safety(cmd_str)

        if self.dry_run:
            return True

        try:
            proc = subprocess.run(
                cmd_list,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=cwd,
                timeout=timeout,
                check=False,
            )
            return proc.returncode == 0
        except Exception:
            return False

    def write_file(self, path: str, content: str, mode: str = 'w', create_dirs: bool = True, permissions: Optional[int] = None) -> None:
        if self.safe_mode:
            self._validate_write_path_safety(path)

        if self.dry_run:
            return

        p = Path(path)

        if create_dirs:
            parent = p.parent
            if parent and not parent.exists():
                parent.mkdir(parents=True, exist_ok=True)

        # Avoid writing through symlinks in safe_mode
        if self.safe_mode and p.exists() and p.is_symlink():
            raise ValueError("Refusing to write to a symlink in safe_mode")

        with p.open(mode, encoding="utf-8") as f:
            f.write(content)

        if permissions is not None:
            os.chmod(p, permissions)

    def _validate_write_path_safety(self, path: str) -> None:
        p = Path(path).resolve()

        critical_dirs = [
            Path("/"),
            Path("/bin"),
            Path("/sbin"),
            Path("/usr"),
            Path("/etc"),
            Path("/lib"),
            Path("/lib64"),
            Path("/boot"),
            Path("/dev"),
            Path("/proc"),
            Path("/sys"),
        ]

        # Windows critical root check (best-effort)
        windows_critical = [
            Path("C:/Windows"),
            Path("C:/Windows/System32"),
        ]

        # Prevent writing directly to critical directories or their immediate critical files
        for c in critical_dirs:
            if p == c or c in p.parents:
                # Allow typical non-system areas like /usr/local, /var/tmp could be legit,
                # but to be conservative, we still block most system trees.
                if str(p).startswith("/usr/local") or str(p).startswith("/var/") or str(p).startswith("/tmp/"):
                    continue
                raise ValueError(
                    f"Refusing to write into critical system path in safe_mode: {p}")

        for c in windows_critical:
            # On non-Windows systems, Path.resolve may not normalize the same, so compare loosely
            if str(p).lower().startswith(str(c).lower()):
                raise ValueError(
                    f"Refusing to write into Windows system path in safe_mode: {p}")

        # Disallow modifying special files
        if p.exists():
            try:
                st = p.lstat()
                if stat.S_ISCHR(st.st_mode) or stat.S_ISBLK(st.st_mode) or stat.S_ISSOCK(st.st_mode) or stat.S_ISFIFO(st.st_mode):
                    raise ValueError(
                        "Refusing to write to special device/socket/FIFO in safe_mode")
            except OSError:
                pass
