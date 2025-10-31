
import logging
import os
import subprocess
from pathlib import Path
from typing import Optional, List


class GitDiffTracker:
    '''Tracks git changes from an initial state through a session.'''

    def __init__(self, enabled: bool = True,
                 logger: Optional[logging.Logger] = None,
                 cwd: Optional[str] = None):
        '''Initialize the git diff tracker.
        Args:
            enabled: Whether to enable git diff tracking (default: True)
            logger: Optional logger instance to use for logging. If not provided,
                    creates a default logger for this module.
            cwd: Working directory for git commands (default: current directory)
        '''
        self.enabled = enabled
        self.cwd = cwd or os.getcwd()
        self.logger = logger or logging.getLogger(__name__)
        self._initial_commit: Optional[str] = None
        if self.enabled:
            self._capture_initial_state()

    def _capture_initial_state(self) -> None:
        '''Capture the initial commit hash to use as a baseline for diffs.'''
        try:
            self._initial_commit = subprocess.check_output(
                ['git', 'rev-parse', 'HEAD'],
                cwd=self.cwd,
                text=True,
                stderr=subprocess.DEVNULL
            ).strip()
            self.logger.debug(
                f'Initial commit captured: {self._initial_commit}')
        except subprocess.SubprocessError as exc:
            self.logger.warning(f'Could not capture initial commit: {exc}')
            self._initial_commit = None

    def get_diff(self) -> Optional[str]:
        '''Get the current git diff from the initial state.
        Returns:
            The git diff output if enabled and there are changes, None otherwise.
        '''
        if not self.enabled or not self._initial_commit:
            return None

        try:
            diff_output = subprocess.check_output(
                ['git', 'diff', self._initial_commit],
                cwd=self.cwd,
                text=True,
                stderr=subprocess.DEVNULL
            ).strip()
        except subprocess.SubprocessError as exc:
            self.logger.warning(f'Error running git diff: {exc}')
            return None

        # Include untracked files
        exclusions = self._get_worktree_exclusions()
        untracked = self._get_untracked_files(exclusions)
        if untracked:
            diff_output = f'{diff_output}\n{untracked}'.strip()

        return diff_output if diff_output else None

    def _get_worktree_exclusions(self) -> List[str]:
        '''Get list of worktree paths to exclude from diff.
        Returns:
            List of exclusion patterns for git commands.
        '''
        # For simplicity, we return an empty list. This can be extended to
        # parse `git worktree list` if needed.
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
                text=True,
                stderr=subprocess.DEVNULL
            ).splitlines()
        except subprocess.SubprocessError as exc:
            self.logger.warning(f'Error listing untracked files: {exc}')
            return ''

        # Apply exclusion patterns if any
        if exclude_patterns:
            filtered = []
            for f in untracked_files:
                if not any(Path(f).match(pat) for pat in exclude_patterns):
                    filtered.append(f)
            untracked_files = filtered

        # Format as diff-like output
        if not untracked_files:
            return ''
        return '\n'.join(f'?? {f}' for f in untracked_files)
