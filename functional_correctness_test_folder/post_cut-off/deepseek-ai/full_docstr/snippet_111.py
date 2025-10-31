
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
        self.logger = logger or logging.getLogger(__name__)
        self.cwd = cwd or os.getcwd()
        self.initial_commit_hash = None
        if self.enabled:
            self._capture_initial_state()

    def _capture_initial_state(self) -> None:
        '''Capture the initial git commit hash if in a git repository.'''
        try:
            result = subprocess.run(
                ['git', 'rev-parse', 'HEAD'],
                cwd=self.cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode == 0:
                self.initial_commit_hash = result.stdout.strip()
        except Exception as e:
            self.logger.warning(f"Failed to capture initial git state: {e}")

    def get_diff(self) -> Optional[str]:
        '''Get the current git diff from the initial state.
        Returns:
            The git diff output if enabled and there are changes, None otherwise.
        '''
        if not self.enabled:
            return None

        try:
            exclude_patterns = self._get_worktree_exclusions()
            diff_output = []

            # Get staged and unstaged changes
            result = subprocess.run(
                ['git', 'diff', '--no-ext-diff', 'HEAD'],
                cwd=self.cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode == 0 and result.stdout.strip():
                diff_output.append(result.stdout)

            # Get untracked files
            untracked = self._get_untracked_files(exclude_patterns)
            if untracked:
                diff_output.append(untracked)

            return '\n'.join(diff_output) if diff_output else None
        except Exception as e:
            self.logger.warning(f"Failed to get git diff: {e}")
            return None

    def _get_worktree_exclusions(self) -> List[str]:
        '''Get list of worktree paths to exclude from diff.
        Returns:
            List of exclusion patterns for git commands.
        '''
        try:
            result = subprocess.run(
                ['git', 'config', '--get-all', 'core.excludesFile'],
                cwd=self.cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            exclude_files = []
            if result.returncode == 0:
                exclude_files = result.stdout.strip().split('\n')
            return exclude_files
        except Exception as e:
            self.logger.warning(f"Failed to get worktree exclusions: {e}")
            return []

    def _get_untracked_files(self, exclude_patterns: List[str]) -> str:
        '''Get untracked files formatted as git diff output.
        Args:
            exclude_patterns: List of patterns to exclude from the output.
        Returns:
            Formatted diff-like output for untracked files.
        '''
        try:
            exclude_args = []
            for pattern in exclude_patterns:
                exclude_args.extend(['--exclude', pattern])

            result = subprocess.run(
                ['git', 'ls-files', '--others', '--exclude-standard'] + exclude_args,
                cwd=self.cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode != 0 or not result.stdout.strip():
                return ""

            untracked_files = result.stdout.strip().split('\n')
            diff_like_output = []
            for file in untracked_files:
                diff_like_output.append(f"diff --git a/{file} b/{file}")
                diff_like_output.append(f"new file mode 100644")
                diff_like_output.append(f"--- /dev/null")
                diff_like_output.append(f"+++ b/{file}")
            return '\n'.join(diff_like_output)
        except Exception as e:
            self.logger.warning(f"Failed to get untracked files: {e}")
            return ""
