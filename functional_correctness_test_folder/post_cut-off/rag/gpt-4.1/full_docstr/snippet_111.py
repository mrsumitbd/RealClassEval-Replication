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
        self.enabled = enabled
        self.logger = logger or logging.getLogger(__name__)
        self.cwd = cwd or os.getcwd()
        self._initial_commit = None
        if self.enabled:
            self._capture_initial_state()

    def _capture_initial_state(self) -> None:
        '''Capture the initial git commit hash if in a git repository.'''
        try:
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=self.cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                text=True
            )
            self._initial_commit = result.stdout.strip()
            self.logger.debug(
                f"Captured initial git commit: {self._initial_commit}")
        except subprocess.CalledProcessError:
            self._initial_commit = None
            self.logger.debug(
                "Not a git repository or unable to get initial commit.")

    def get_diff(self) -> Optional[str]:
        '''Get the current git diff from the initial state.
        Returns:
            The git diff output if enabled and there are changes, None otherwise.
        '''
        if not self.enabled or not self._initial_commit:
            return None

        exclude_patterns = self._get_worktree_exclusions()
        diff_cmd = ["git", "diff", self._initial_commit, "--"]
        for pat in exclude_patterns:
            diff_cmd.extend([":(exclude)" + pat])

        try:
            result = subprocess.run(
                diff_cmd,
                cwd=self.cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                text=True
            )
            diff_output = result.stdout
        except subprocess.CalledProcessError as e:
            self.logger.warning(f"Failed to get git diff: {e}")
            return None

        untracked = self._get_untracked_files(exclude_patterns)
        combined = (diff_output or "") + (untracked or "")
        if combined.strip():
            return combined
        return None

    def _get_worktree_exclusions(self) -> List[str]:
        '''Get list of worktree paths to exclude from diff.
        Returns:
            List of exclusion patterns for git commands.
        '''
        # Example: exclude .git and .venv directories
        exclusions = [".git", ".venv", "venv", "__pycache__"]
        self.logger.debug(f"Worktree exclusions: {exclusions}")
        return exclusions

    def _get_untracked_files(self, exclude_patterns: List[str]) -> str:
        '''Get untracked files formatted as git diff output.
        Args:
            exclude_patterns: List of patterns to exclude from the output.
        Returns:
            Formatted diff-like output for untracked files.
        '''
        cmd = ["git", "ls-files", "--others", "--exclude-standard"]
        for pat in exclude_patterns:
            cmd.extend(["--exclude", pat])
        try:
            result = subprocess.run(
                cmd,
                cwd=self.cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                text=True
            )
            files = [f for f in result.stdout.splitlines() if f.strip()]
            if not files:
                return ""
            output = []
            for f in files:
                output.append(f"diff --git a/{f} b/{f}\n")
                output.append(f"new file mode 100644\n")
                output.append(f"--- /dev/null\n")
                output.append(f"+++ b/{f}\n")
                try:
                    with open(os.path.join(self.cwd, f), "r", encoding="utf-8", errors="replace") as fh:
                        lines = fh.readlines()
                    for line in lines:
                        output.append(f"+{line.rstrip()}\n")
                except Exception:
                    output.append("+[binary or unreadable file]\n")
            return "".join(output)
        except subprocess.CalledProcessError as e:
            self.logger.warning(f"Failed to get untracked files: {e}")
            return ""
