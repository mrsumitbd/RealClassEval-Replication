import logging
import os
import subprocess
from typing import Optional, List
import fnmatch


class GitDiffTracker:

    def __init__(self, enabled: bool = True, logger: Optional[logging.Logger] = None, cwd: Optional[str] = None):
        self.enabled = enabled
        self.logger = logger or logging.getLogger(__name__)
        self.cwd = cwd or os.getcwd()
        self._repo_available = False
        self._initial_head = None

        if not self.enabled:
            return

        try:
            result = subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"],
                cwd=self.cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
            )
            self._repo_available = result.stdout.strip() == "true"
        except Exception:
            self._repo_available = False
            self.enabled = False
            return

        if self._repo_available:
            self._capture_initial_state()
        else:
            self.enabled = False

    def _capture_initial_state(self) -> None:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=self.cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
            )
            self._initial_head = result.stdout.strip()
        except Exception:
            self._initial_head = None

    def get_diff(self) -> Optional[str]:
        if not self.enabled or not self._repo_available:
            return None

        try:
            diff_unstaged = subprocess.run(
                ["git", "diff", "--patch", "--no-color"],
                cwd=self.cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            ).stdout
        except Exception:
            diff_unstaged = ""

        try:
            diff_staged = subprocess.run(
                ["git", "diff", "--patch", "--no-color", "--cached"],
                cwd=self.cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            ).stdout
        except Exception:
            diff_staged = ""

        exclude_patterns = self._get_worktree_exclusions()
        try:
            untracked_patch = self._get_untracked_files(exclude_patterns)
        except Exception:
            untracked_patch = ""

        combined = []
        if diff_staged.strip():
            combined.append(diff_staged.strip())
        if diff_unstaged.strip():
            combined.append(diff_unstaged.strip())
        if untracked_patch.strip():
            combined.append(untracked_patch.strip())

        if not combined:
            return None
        return "\n\n".join(combined) + "\n"

    def _get_worktree_exclusions(self) -> list[str]:
        patterns: List[str] = []
        # .git/info/exclude
        git_dir = None
        try:
            git_dir = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                cwd=self.cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
            ).stdout.strip()
        except Exception:
            git_dir = None

        if git_dir:
            info_exclude = os.path.join(self.cwd, git_dir, "info", "exclude")
            if os.path.isfile(info_exclude):
                try:
                    with open(info_exclude, "r", encoding="utf-8", errors="ignore") as f:
                        for line in f:
                            s = line.strip()
                            if not s or s.startswith("#"):
                                continue
                            patterns.append(s)
                except Exception:
                    pass

        return patterns

    def _get_untracked_files(self, exclude_patterns: list[str]) -> str:
        try:
            # git will already honor .gitignore and core excludes
            result = subprocess.run(
                ["git", "ls-files", "--others", "--exclude-standard"],
                cwd=self.cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
            )
            files = [line.strip()
                     for line in result.stdout.splitlines() if line.strip()]
        except Exception:
            files = []

        if not files:
            return ""

        def is_excluded(path: str) -> bool:
            # Apply additional exclude patterns (best-effort using fnmatch)
            # Patterns are considered relative to repo root
            for pat in exclude_patterns:
                if fnmatch.fnmatch(path, pat):
                    return True
            return False

        patches = []
        for relpath in files:
            if is_excluded(relpath):
                continue
            abspath = os.path.join(self.cwd, relpath)
            if not os.path.isfile(abspath):
                continue
            try:
                with open(abspath, "rb") as fb:
                    data = fb.read()
            except Exception:
                # If not readable, skip
                continue

            # Detect binary
            is_binary = b"\x00" in data or any(b > 0x7F for b in data[:1024])
            if is_binary:
                header = [
                    f"diff --git a/{relpath} b/{relpath}",
                    f"new file mode 100644",
                    f"index 0000000..0000000",
                    f"--- /dev/null",
                    f"+++ b/{relpath}",
                    f"Binary files differ",
                ]
                patches.append("\n".join(header))
                continue

            try:
                text = data.decode("utf-8")
            except UnicodeDecodeError:
                # Fall back to latin-1 to avoid failure; still treated as text
                text = data.decode("latin-1")

            lines = text.splitlines()
            # In unified diff, added file: from /dev/null to file with all lines prefixed by +
            # Count lines for hunk header
            n = len(lines)
            header = [
                f"diff --git a/{relpath} b/{relpath}",
                f"new file mode 100644",
                f"index 0000000..0000000",
                f"--- /dev/null",
                f"+++ b/{relpath}",
                f"@@ -0,0 +1,{n} @@",
            ]
            content = [f"+{l}" for l in lines]
            # Ensure newline at end of file is not strictly enforced; this is a best-effort patch
            patches.append("\n".join(header + content))

        return "\n\n".join(patches) if patches else ""
