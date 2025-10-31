
import logging
import subprocess
from typing import Optional


class GitDiffTracker:
    """Tracks git changes from an initial state through a session."""

    def __init__(self, enabled: bool = True, logger: Optional[logging.Logger] = None, cwd: Optional[str] = None):
        """Initialize the git diff tracker.

        Args:
            enabled: Whether to enable git diff tracking (default: True)
            logger: Optional logger instance to use for logging. If not provided,
                    creates a default logger for this module.
            cwd: Working directory for git commands (default: current directory)
        """
        self.enabled = enabled
        self.logger = logger or logging.getLogger(__name__)
        self.cwd = cwd or '.'
        self.initial_commit_hash = None
        if enabled:
            self._capture_initial_state()

    def _capture_initial_state(self) -> None:
        """Capture the initial git commit hash if in a git repository."""
        try:
            self.initial_commit_hash = subprocess.check_output(
                ['git', 'rev-parse', 'HEAD'], cwd=self.cwd).decode().strip()
        except subprocess.CalledProcessError:
            self.logger.warning(
                'Not a git repository, git diff tracking disabled')
            self.enabled = False

    def get_diff(self) -> Optional[str]:
        """Get the current git diff from the initial state.

        Returns:
            The git diff output if enabled and there are changes, None otherwise.
        """
        if not self.enabled:
            return None

        try:
            exclude_patterns = self._get_worktree_exclusions()
            untracked_files = self._get_untracked_files(exclude_patterns)
            diff_output = subprocess.check_output(
                ['git', 'diff', self.initial_commit_hash] + exclude_patterns, cwd=self.cwd).decode()
            if untracked_files:
                diff_output += '\n' + untracked_files
            return diff_output if diff_output else None
        except subprocess.CalledProcessError as e:
            self.logger.error('Failed to get git diff: %s', e)
            return None

    def _get_worktree_exclusions(self) -> list[str]:
        """Get list of worktree paths to exclude from diff.

        Returns:
            List of exclusion patterns for git commands.
        """
        try:
            worktree_output = subprocess.check_output(
                ['git', 'worktree', 'list', '--porcelain'], cwd=self.cwd).decode().splitlines()
            exclusions = []
            for line in worktree_output:
                if line.startswith('worktree'):
                    worktree_path = line.split()[1]
                    exclusions.extend(['--exclude', worktree_path])
            return exclusions
        except subprocess.CalledProcessError:
            return []

    def _get_untracked_files(self, exclude_patterns: list[str]) -> str:
        """Get untracked files formatted as git diff output.

        Args:
            exclude_patterns: List of patterns to exclude from the output.

        Returns:
            Formatted diff-like output for untracked files.
        """
        try:
            untracked_files_output = subprocess.check_output(
                ['git', 'ls-files', '--others', '--exclude-standard'] + exclude_patterns, cwd=self.cwd).decode().splitlines()
            diff_output = []
            for file in untracked_files_output:
                file_contents = subprocess.check_output(
                    ['cat', file], cwd=self.cwd).decode()
                diff_output.append(
                    f'diff --git a/{file} b/{file}\nnew file mode 100644\nindex 0000000..{hash(file_contents.encode()):x}\n--- /dev/null\n+++ b/{file}\n@@ -0,0 +1 @@\n+{file_contents}')
            return '\n'.join(diff_output)
        except subprocess.CalledProcessError:
            return ''
