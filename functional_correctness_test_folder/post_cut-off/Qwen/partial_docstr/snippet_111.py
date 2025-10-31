
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
        self.initial_state = None
        if self.enabled:
            self._capture_initial_state()

    def _capture_initial_state(self) -> None:
        try:
            self.initial_state = subprocess.check_output(
                ['git', 'diff-index', '--cached', 'HEAD', '--'],
                cwd=self.cwd,
                stderr=subprocess.STDOUT
            ).decode('utf-8')
        except subprocess.CalledProcessError as e:
            self.logger.error(
                f"Failed to capture initial git state: {e.output.decode('utf-8')}")
            self.initial_state = None

    def get_diff(self) -> Optional[str]:
        '''Get the current git diff from the initial state.
        Returns:
            The git diff output if enabled and there are changes, None otherwise.
        '''
        if not self.enabled or self.initial_state is None:
            return None
        try:
            current_state = subprocess.check_output(
                ['git', 'diff-index', '--cached', 'HEAD', '--'],
                cwd=self.cwd,
                stderr=subprocess.STDOUT
            ).decode('utf-8')
            untracked_files = self._get_untracked_files(
                self._get_worktree_exclusions())
            if current_state or untracked_files:
                return current_state + untracked_files
        except subprocess.CalledProcessError as e:
            self.logger.error(
                f"Failed to get git diff: {e.output.decode('utf-8')}")
        return None

    def _get_worktree_exclusions(self) -> List[str]:
        '''Get list of worktree paths to exclude from diff.
        Returns:
            List of exclusion patterns for git commands.
        '''
        try:
            worktrees = subprocess.check_output(
                ['git', 'worktree', 'list', '--porcelain'],
                cwd=self.cwd,
                stderr=subprocess.STDOUT
            ).decode('utf-8').splitlines()
            exclusions = []
            for line in worktrees:
                if line.startswith('worktree'):
                    exclusions.append(line.split()[1])
            return exclusions
        except subprocess.CalledProcessError as e:
            self.logger.error(
                f"Failed to get worktree exclusions: {e.output.decode('utf-8')}")
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
                ['git', 'ls-files', '--others',
                    '--exclude-standard'] + exclude_patterns,
                cwd=self.cwd,
                stderr=subprocess.STDOUT
            ).decode('utf-8').splitlines()
            diff_output = ''
            for file in untracked_files:
                diff_output += f"Untracked file: {file}\n"
            return diff_output
        except subprocess.CalledProcessError as e:
            self.logger.error(
                f"Failed to get untracked files: {e.output.decode('utf-8')}")
            return ''
