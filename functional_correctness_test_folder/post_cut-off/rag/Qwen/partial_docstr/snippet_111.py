
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
        self.initial_commit_hash = None
        if self.enabled:
            self._capture_initial_state()

    def _capture_initial_state(self) -> None:
        '''Capture the initial git commit hash if in a git repository.'''
        try:
            self.initial_commit_hash = subprocess.check_output(
                ['git', 'rev-parse', 'HEAD'],
                cwd=self.cwd,
                stderr=subprocess.STDOUT
            ).strip().decode('utf-8')
        except subprocess.CalledProcessError:
            self.logger.warning(
                "Not in a git repository or unable to capture initial commit hash.")
            self.initial_commit_hash = None

    def get_diff(self) -> Optional[str]:
        '''Get the current git diff from the initial state.
        Returns:
            The git diff output if enabled and there are changes, None otherwise.
        '''
        if not self.enabled or self.initial_commit_hash is None:
            return None
        try:
            exclude_patterns = self._get_worktree_exclusions()
            diff_output = subprocess.check_output(
                ['git', 'diff', self.initial_commit_hash, '--'] + exclude_patterns,
                cwd=self.cwd,
                stderr=subprocess.STDOUT
            ).decode('utf-8')
            untracked_files_diff = self._get_untracked_files(exclude_patterns)
            if untracked_files_diff:
                diff_output += untracked_files_diff
            return diff_output if diff_output.strip() else None
        except subprocess.CalledProcessError as e:
            self.logger.error(
                f"Error getting git diff: {e.output.decode('utf-8')}")
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
            exclude_patterns = []
            for line in worktrees:
                if line.startswith('worktree'):
                    path = line.split()[1]
                    exclude_patterns.append(
                        f':(exclude){os.path.relpath(path, self.cwd)}/*')
            return exclude_patterns
        except subprocess.CalledProcessError:
            self.logger.warning("Failed to get worktree paths for exclusion.")
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
            diff_output = ""
            for file in untracked_files:
                diff_output += f"Untracked file: {file}\n"
            return diff_output if diff_output else ""
        except subprocess.CalledProcessError:
            self.logger.warning("Failed to get untracked files.")
            return ""
