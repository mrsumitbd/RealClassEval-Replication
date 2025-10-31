
import logging
import subprocess
import os
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
        self.logger = logger if logger else logging.getLogger(__name__)
        self.cwd = cwd if cwd else os.getcwd()
        self._initial_diff = None
        if self.enabled:
            self._capture_initial_state()

    def _capture_initial_state(self) -> None:
        '''Capture the initial git diff state.'''
        try:
            self._initial_diff = self._get_current_diff()
        except subprocess.CalledProcessError as e:
            self.logger.warning(f"Failed to capture initial git state: {e}")
            self._initial_diff = None

    def get_diff(self) -> Optional[str]:
        '''Get the current git diff from the initial state.
        Returns:
            The git diff output if enabled and there are changes, None otherwise.
        '''
        if not self.enabled or not self._initial_diff:
            return None
        try:
            current_diff = self._get_current_diff()
            if current_diff != self._initial_diff:
                return current_diff
        except subprocess.CalledProcessError as e:
            self.logger.warning(f"Failed to get git diff: {e}")
        return None

    def _get_current_diff(self) -> str:
        '''Get the current git diff including untracked files.
        Returns:
            Combined diff output for tracked and untracked files.
        '''
        exclude_patterns = self._get_worktree_exclusions()
        tracked_diff = subprocess.check_output(
            ['git', 'diff'],
            cwd=self.cwd,
            text=True
        ).strip()
        untracked_diff = self._get_untracked_files(exclude_patterns)
        return f"{tracked_diff}\n{untracked_diff}".strip()

    def _get_worktree_exclusions(self) -> List[str]:
        '''Get list of worktree paths to exclude from diff.
        Returns:
            List of exclusion patterns for git commands.
        '''
        return []

    def _get_untracked_files(self, exclude_patterns: List[str]) -> str:
        '''Get untracked files formatted as git diff output.
        Args:
            exclude_patterns: List of patterns to exclude from the output.
        Returns:
            Formatted diff-like output for untracked files.
        '''
        try:
            untracked_files = subprocess.check_output(
                ['git', 'ls-files', '--others', '--exclude-standard'],
                cwd=self.cwd,
                text=True
            ).splitlines()
            if not untracked_files:
                return ""
            diff_output = []
            for file in untracked_files:
                if not any(file.startswith(pattern) for pattern in exclude_patterns):
                    diff_output.append(f"diff --git a/{file} b/{file}")
                    diff_output.append(f"new file mode 100644")
                    diff_output.append(f"--- /dev/null")
                    diff_output.append(f"+++ b/{file}")
            return "\n".join(diff_output)
        except subprocess.CalledProcessError as e:
            self.logger.warning(f"Failed to get untracked files: {e}")
            return ""
