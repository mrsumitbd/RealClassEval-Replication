import logging
import os
import subprocess
from pathlib import Path
from typing import Optional, List
import fnmatch


class GitDiffTracker:
    '''Tracks git changes from an initial state through a session.'''

    def __init__(self, enabled: bool = True, logger: Optional[logging.Logger] = None, cwd: Optional[str] = None):
        '''Initialize the git diff tracker.
        Args:
            enabled: Whether to enable git diff tracking (default: True)
            logger: Optional logger instance to use for logging. If not provided,
                    creates a default logger for this module.
            cwd: Working directory for git commands (default: current directory)
        '''
        self.enabled = bool(enabled)
        self.cwd = Path(cwd).resolve() if cwd else Path.cwd().resolve()
        self.logger = logger or logging.getLogger(__name__)
        if not logger:
            if not self.logger.handlers:
                handler = logging.StreamHandler()
                formatter = logging.Formatter(
                    '%(levelname)s:%(name)s:%(message)s')
                handler.setFormatter(formatter)
                self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

        self._is_repo = False
        self._repo_root: Optional[Path] = None
        self._exclude_patterns: List[str] = []
        self._initial_captured: bool = False

        if self.enabled:
            self._capture_initial_state()

    def _run_git(self, args: list[str], check: bool = False, capture_output: bool = True) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["git", *args],
            cwd=str(self.cwd),
            check=check,
            capture_output=capture_output,
            text=True,
        )

    def _capture_initial_state(self) -> None:
        try:
            p = self._run_git(["rev-parse", "--is-inside-work-tree"])
            self._is_repo = p.returncode == 0 and p.stdout.strip() == "true"
            if not self._is_repo:
                return
            root = self._run_git(["rev-parse", "--show-toplevel"])
            if root.returncode == 0:
                self._repo_root = Path(root.stdout.strip()).resolve()
            else:
                self._repo_root = self.cwd
            self._exclude_patterns = self._get_worktree_exclusions()
            self._initial_captured = True
        except Exception as e:
            self.logger.debug(f"Failed to capture initial git state: {e}")
            self._is_repo = False

    def get_diff(self) -> Optional[str]:
        '''Get the current git diff from the initial state.
        Returns:
            The git diff output if enabled and there are changes, None otherwise.
        '''
        if not self.enabled or not self._is_repo:
            return None

        # Tracked changes vs HEAD (includes staged and unstaged changes)
        tracked = self._run_git(["diff", "HEAD"])
        tracked_diff = tracked.stdout if tracked.returncode in (0, 1) else ""

        # Untracked files formatted like diff
        untracked_diff = self._get_untracked_files(self._exclude_patterns)

        combined = ""
        if tracked_diff.strip():
            combined += tracked_diff
            if not tracked_diff.endswith("\n"):
                combined += "\n"
        if untracked_diff.strip():
            combined += untracked_diff

        return combined if combined.strip() else None

    def _get_worktree_exclusions(self) -> list[str]:
        '''Get list of worktree paths to exclude from diff.
        Returns:
            List of exclusion patterns for git commands.
        '''
        patterns: list[str] = []
        if not self._is_repo or not self._repo_root:
            return patterns
        try:
            res = self._run_git(["worktree", "list", "--porcelain"])
            if res.returncode != 0:
                return patterns
            lines = res.stdout.splitlines()
            worktree_paths: list[Path] = []
            for line in lines:
                if line.startswith("worktree "):
                    path = line.split(" ", 1)[1].strip()
                    p = Path(path).resolve()
                    worktree_paths.append(p)
            for wt in worktree_paths:
                try:
                    rel = os.path.relpath(wt, self._repo_root)
                    # Normalize separators to forward slash for fnmatch consistency
                    rel_norm = rel.replace(os.sep, "/")
                    # Exclude the worktree directory itself and its subtree
                    patterns.append(rel_norm)
                    if not rel_norm.endswith("/"):
                        patterns.append(rel_norm + "/**")
                except ValueError:
                    # If not relative (on different drive), exclude by absolute pattern
                    patterns.append(str(wt))
                    patterns.append(str(wt) + "/**")
            # Also exclude the .git directory by default
            patterns.append(".git")
            patterns.append(".git/**")
        except Exception as e:
            self.logger.debug(f"Failed to get worktree exclusions: {e}")
        return patterns

    def _path_matches_any_pattern(self, path: str, patterns: list[str]) -> bool:
        norm = path.replace(os.sep, "/")
        for pat in patterns:
            if fnmatch.fnmatch(norm, pat):
                return True
        return False

    def _get_untracked_files(self, exclude_patterns: list[str]) -> str:
        '''Get untracked files formatted as git diff output.
        Args:
            exclude_patterns: List of patterns to exclude from the output.
        Returns:
            Formatted diff-like output for untracked files.
        '''
        if not self._is_repo or not self._repo_root:
            return ""
        try:
            res = self._run_git(
                ["ls-files", "--others", "--exclude-standard", "-z"])
            if res.returncode != 0:
                return ""
            entries = [e for e in res.stdout.split("\x00") if e]
            # Filter by exclusion patterns
            filtered: list[str] = []
            for e in entries:
                if not self._path_matches_any_pattern(e, exclude_patterns):
                    filtered.append(e)

            diffs: list[str] = []
            for rel in filtered:
                full = self._repo_root / rel
                # Skip directories; git may not list directories, but be safe
                if not full.exists() or full.is_dir():
                    continue
                # Use git diff --no-index to generate a patch from /dev/null to the file
                # This handles binaries by printing a binary notice
                try:
                    proc = subprocess.run(
                        ["git", "diff", "--no-index",
                            "--", "/dev/null", str(full)],
                        cwd=str(self._repo_root),
                        text=True,
                        capture_output=True,
                    )
                    if proc.returncode in (0, 1):  # 1 indicates differences found
                        out = proc.stdout
                        if out.strip():
                            diffs.append(out if out.endswith(
                                "\n") else out + "\n")
                except Exception as e:
                    self.logger.debug(
                        f"Failed to diff untracked file {rel}: {e}")
            return "".join(diffs)
        except Exception as e:
            self.logger.debug(f"Failed to get untracked files: {e}")
            return ""
