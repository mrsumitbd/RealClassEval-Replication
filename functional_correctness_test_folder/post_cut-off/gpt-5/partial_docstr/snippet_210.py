from typing import Optional
import os
import re
import subprocess


class Shell:
    '''Wrapper around subprocess supporting dry_run mode.'''

    def __init__(self, dry_run: bool = False, safe_mode: bool = True):
        '''Initialize shell wrapper.
        Args:
            dry_run: If True, commands will be logged but not executed
            safe_mode: If True, enables additional safety checks for commands
        '''
        self.dry_run = dry_run
        self.safe_mode = safe_mode

    def _validate_command_safety(self, cmd: str) -> None:
        '''Validate command for basic safety if safe_mode is enabled.
        Args:
            cmd: Command to validate
        Raises:
            RuntimeError: If command appears unsafe
        '''
        if not self.safe_mode:
            return

        c = cmd.strip()
        cl = c.lower()

        if not c:
            raise RuntimeError("Unsafe/invalid command: empty command")

        # Fork bomb
        if ':()' in c.replace(' ', '') or ':(){' in c:
            raise RuntimeError(
                "Unsafe command in safe_mode: fork bomb pattern detected")

        # Dangerous system power commands
        power_cmds = [
            r'\bshutdown\b', r'\breboot\b', r'\bhalt\b', r'\bpoweroff\b',
            r'\binit\s+0\b', r'\bsystemctl\s+(poweroff|reboot|halt)\b'
        ]
        # Filesystem destroyers / partitioning tools
        disk_tools = [
            r'\bmkfs(\.\w+)?\b', r'\bfdisk\b', r'\bparted\b', r'\bwipefs\b',
            r'\bcryptsetup\b.*\b(format|luksFormat)\b', r'\blvm\b', r'\bvg(remove|destroy)\b', r'\bmdadm\b.*(--create|--zero-superblock)'
        ]
        # Kill critical PID 1
        critical_kill = [r'\bkill\s+(-9\s+)?1\b']

        for pat in power_cmds + disk_tools + critical_kill:
            if re.search(pat, cl):
                raise RuntimeError(
                    f"Unsafe command in safe_mode: matches pattern '{pat}'")

        # rm -rf / or /* patterns
        if re.search(r'\brm\b', cl):
            if re.search(r'\brm\b.*\b(-rf|-fr|--recursive)\b', cl):
                if re.search(r'\s/(\s|$)', c) or re.search(r'/\*', c):
                    raise RuntimeError(
                        "Unsafe command in safe_mode: destructive rm against /")

        # dd or redirection to raw block devices
        block_dev_pat = r'/dev/(sd\w+|nvme\d+n\d+(p\d+)?|mmcblk\d+p?\d*|loop\d+|vd\w+|xvd\w+)'
        if re.search(r'\bdd\b', cl) and re.search(rf'of\s*=\s*{block_dev_pat}', c):
            raise RuntimeError(
                "Unsafe command in safe_mode: dd writing to block device")
        if re.search(rf'>\s*{block_dev_pat}', c) or re.search(rf'>>\s*{block_dev_pat}', c) or re.search(rf'>\|\s*{block_dev_pat}', c):
            raise RuntimeError(
                "Unsafe command in safe_mode: redirect to block device")

        # Chmod/chown recursively on root
        if re.search(r'\bchown\b.*\s-R\b.*\s/(\s|$)', cl) or re.search(r'\bchmod\b.*\s-R\b.*\s/(\s|$)', cl):
            raise RuntimeError(
                "Unsafe command in safe_mode: recursive chown/chmod on /")

    def run(self, *parts: str, timeout: int = 30, cwd: Optional[str] = None) -> str:
        '''Execute a shell command and return stripped output.
        Args:
            *parts: Command parts to join with spaces
            timeout: Command timeout in seconds
            cwd: Working directory for command execution
        Returns:
            Command output as string
        Raises:
            RuntimeError: If command fails or times out
        '''
        cmd = " ".join(p for p in parts if p is not None)
        self._validate_command_safety(cmd)

        if self.dry_run:
            print(f"[dry-run] would run: {cmd}")
            return ""

        try:
            res = subprocess.run(
                cmd,
                shell=True,
                cwd=cwd,
                timeout=timeout,
                text=True,
                capture_output=True,
                encoding='utf-8',
                errors='replace'
            )
        except subprocess.TimeoutExpired as e:
            raise RuntimeError(
                f"Command timed out after {timeout}s: {cmd}") from e
        except Exception as e:
            raise RuntimeError(f"Failed to execute command: {cmd}") from e

        if res.returncode != 0:
            stderr = (res.stderr or "").strip()
            raise RuntimeError(
                f"Command failed (exit {res.returncode}): {cmd}\n{stderr}")

        return (res.stdout or "").strip()

    def run_check(self, *parts: str, timeout: int = 30, cwd: Optional[str] = None) -> bool:
        if self.dry_run:
            cmd = " ".join(p for p in parts if p is not None)
            self._validate_command_safety(cmd)
            print(f"[dry-run] would run (check): {cmd}")
            return True

        cmd = " ".join(p for p in parts if p is not None)
        self._validate_command_safety(cmd)
        try:
            res = subprocess.run(
                cmd,
                shell=True,
                cwd=cwd,
                timeout=timeout,
                text=True,
                capture_output=True,
                encoding='utf-8',
                errors='replace'
            )
        except subprocess.TimeoutExpired as e:
            raise RuntimeError(
                f"Command timed out after {timeout}s: {cmd}") from e
        except Exception as e:
            raise RuntimeError(f"Failed to execute command: {cmd}") from e

        return res.returncode == 0

    def write_file(self, path: str, content: str, mode: str = 'w', create_dirs: bool = True, permissions: Optional[int] = None) -> None:
        '''Write content to a file (respects dry_run mode).
        Args:
            path: File path to write to
            content: Content to write
            mode: File write mode (default: "w")
            create_dirs: Create parent directories if they don't exist
            permissions: Unix file permissions (e.g., 0o600 for user-only)
        Raises:
            RuntimeError: If file operation fails
        '''
        if 'b' in mode:
            raise RuntimeError(
                "Binary mode not supported; provide text content")

        directory = os.path.dirname(os.path.abspath(path))
        if create_dirs and directory and not os.path.exists(directory):
            if self.dry_run:
                print(f"[dry-run] would create directories: {directory}")
            else:
                try:
                    os.makedirs(directory, exist_ok=True)
                except Exception as e:
                    raise RuntimeError(
                        f"Failed to create directories for {path}") from e

        if self.dry_run:
            print(
                f"[dry-run] would write file: {path} (mode={mode}, permissions={permissions})")
            return

        try:
            with open(path, mode, encoding='utf-8') as f:
                f.write(content)
            if permissions is not None:
                os.chmod(path, permissions)
        except Exception as e:
            raise RuntimeError(f"Failed to write file {path}") from e
