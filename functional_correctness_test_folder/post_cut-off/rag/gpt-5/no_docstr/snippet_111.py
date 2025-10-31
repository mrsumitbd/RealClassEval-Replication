import logging
import os
import subprocess
from typing import Optional, List


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
        self.logger = logger or logging.getLogger(__name__)
        self.cwd = cwd or os.getcwd()
        self.in_repo = False
        self.repo_root: Optional[str] = None
        self.initial_commit: Optional[str] = None

        if self.enabled:
            self._capture_initial_state()

    def _run_git(self, args: List[str], allow_rc: Optional[set[int]] = None) -> subprocess.CompletedProcess:
        if allow_rc is None:
            allow_rc = {0}
        cp = subprocess.run(
            ["git"] + args,
            cwd=self.cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
        )
        if cp.returncode not in allow_rc:
            self.logger.debug("git command failed: git %s (rc=%s, stderr=%s)", " ".join(
                args), cp.returncode, cp.stderr.strip())
        else:
            self.logger.debug("git %s -> rc=%s", " ".join(args), cp.returncode)
        return cp

    def _capture_initial_state(self) -> None:
        '''Capture the initial git commit hash if in a git repository.'''
        try:
            cp = self._run_git(["rev-parse", "--is-inside-work-tree"])
            if cp.returncode != 0 or cp.stdout.strip().lower() != "true":
                self.in_repo = False
                return
            self.in_repo = True

            root_cp = self._run_git(["rev-parse", "--show-toplevel"])
            if root_cp.returncode == 0:
                self.repo_root = root_cp.stdout.strip()
            else:
                self.repo_root = None

            head_cp = self._run_git(["rev-parse", "HEAD"])
            if head_cp.returncode == 0:
                self.initial_commit = head_cp.stdout.strip()
            else:
                self.initial_commit = None
        except Exception as exc:
            self.logger.debug("Failed to capture initial git state: %s", exc)
            self.in_repo = False
            self.repo_root = None
            self.initial_commit = None

    def get_diff(self) -> Optional[str]:
        '''Get the current git diff from the initial state.
        Returns:
            The git diff output if enabled and there are changes, None otherwise.
        '''
        if not self.enabled or not self.in_repo:
            return None

        exclusions = self._get_worktree_exclusions()
        pathspec_excludes = [f":(exclude){p}" for p in exclusions]

        diff_output = ""

        if self.initial_commit:
            args = ["diff", "--no-ext-diff", self.initial_commit, "--"]
            args.extend(pathspec_excludes)
            cp = self._run_git(args)
            if cp.returncode == 0:
                diff_output += cp.stdout
            else:
                # Even without --exit-code, nonzero can happen in some error scenarios; we already logged debug
                pass
        else:
            # Fallback: no initial commit (e.g., empty repo). Show working tree differences.
            cp = self._run_git(["diff", "--no-ext-diff"])
            if cp.returncode == 0:
                diff_output += cp.stdout

        # Append untracked file diffs
        diff_output += self._get_untracked_files(exclusions)

        diff_output = diff_output.strip()
        return diff_output if diff_output else None

    def _get_worktree_exclusions(self) -> list[str]:
        '''Get list of worktree paths to exclude from diff.
        Returns:
            List of exclusion patterns for git commands.
        '''
        if not self.in_repo or not self.repo_root:
            return []

        cp = self._run_git(["worktree", "list", "--porcelain"])
        if cp.returncode != 0:
            return []

        exclusions: list[str] = []
        current = os.path.normpath(self.repo_root)

        for line in cp.stdout.splitlines():
            if line.startswith("worktree "):
                wt_path = line.split(" ", 1)[1].strip()
                wt_path = os.path.normpath(wt_path)
                if wt_path == current:
                    continue
                # If the worktree is a subpath of the current repo root, exclude it
                try:
                    rel = os.path.relpath(wt_path, start=current)
                except ValueError:
                    # On different drives (Windows) or unrelated paths; ignore
                    continue
                if not rel.startswith(".."):
                    exclusions.append(rel)
        return exclusions

    def _get_untracked_files(self, exclude_patterns: list[str]) -> str:
        '''Get untracked files formatted as git diff output.
        Args:
            exclude_patterns: List of patterns to exclude from the output.
        Returns:
            Formatted diff-like output for untracked files.
        '''
        if not self.in_repo or not self.repo_root:
            return ""

        # List untracked files (null-separated)
        cp = self._run_git(
            ["ls-files", "--others", "--exclude-standard", "-z"])
        if cp.returncode != 0:
            return ""

        output_chunks: list[str] = []
        entries = [e for e in cp.stdout.split("\x00") if e]

        def is_excluded(path: str) -> bool:
            path_norm = path.replace("\\", "/")
            for pat in exclude_patterns:
                pat_norm = pat.rstrip("/").replace("\\", "/")
                if path_norm == pat_norm or path_norm.startswith(pat_norm + "/"):
                    return True
            return False

        for relpath in entries:
            if is_excluded(relpath):
                continue
            # Generate a diff against /dev/null for each untracked file.
            # Use --no-index to force a raw file diff.
            try:
                cp_diff = subprocess.run(
                    ["git", "diff", "--no-index", "--", "/dev/null", relpath],
                    cwd=self.repo_root,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    encoding="utf-8",
                )
                # git diff --no-index returns 1 when there are differences; accept 0 or 1.
                if cp_diff.returncode in (0, 1):
                    if cp_diff.stdout:
                        output_chunks.append(cp_diff.stdout)
                else:
                    self.logger.debug(
                        "git diff --no-index failed for %s: rc=%s, stderr=%s",
                        relpath, cp_diff.returncode, cp_diff.stderr.strip(),
                    )
            except Exception as exc:
                self.logger.debug(
                    "Failed to diff untracked file %s: %s", relpath, exc)

        return "".join(output_chunks)
