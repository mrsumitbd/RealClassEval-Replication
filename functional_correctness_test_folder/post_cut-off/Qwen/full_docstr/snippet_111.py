
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
        self.initial_commit = None
        if self.enabled:
            self._capture_initial_state()

    def _capture_initial_state(self) -> None:
        '''Capture the initial git commit hash if in a git repository.'''
        try:
            self.initial_commit = subprocess.check_output(
                ['git', 'rev-parse', 'HEAD'],
                cwd=self.cwd,
                stderr=subprocess.STDOUT
            ).strip().decode('utf-8')
        except subprocess.CalledProcessError:
            self.logger.warning(
                "Not in a git repository or unable to capture initial commit hash.")
            self.initial_commit = None

    def get_diff(self) -> Optional[str]:
        '''Get the current git diff from the initial state.
        Returns:
            The git diff output if enabled and there are changes, None otherwise.
        '''
        if not self.enabled or self.initial_commit is None:
            return None
        try:
            diff_output = subprocess.check_output(
                ['git', 'diff', self.initial_commit],
                cwd=self.cwd,
                stderr=subprocess.STDOUT
            ).decode('utf-8')
            untracked_files = self._get_untracked_files(
                self._get_worktree_exclusions())
            if untracked_files:
                diff_output += f"\nUntracked files:\n{untracked_files}"
            return diff_output if diff_output.strip() else None
        except subprocess.CalledProcessError as e:
            self.logger.error(
                f"Error retrieving git diff: {e.output.decode('utf-8')}")
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
                    exclusions.append(line.split()[1].strip())
            return exclusions
        except subprocess.CalledProcessError:
            self.logger.warning("Failed to retrieve worktree paths.")
            return []

    def _get_untracked_files(self, exclude_patterns: List[str]) -> str:
        '''Get untracked files formatted as git diff output.
        Args:
            exclude_patterns: List of patterns to exclude from the output.
        Returns:
            Formatted diff-like output for untracked files.
        '''
        try:
            untracked_output = subprocess.check_output(
                ['git', 'ls-files', '--others', '--exclude-standard'] +
                [f'--exclude={p}' for p in exclude_patterns],
                cwd=self.cwd,
                stderr=subprocess.STDOUT
            ).decode('utf-8').splitlines()
            if not untracked_output:
                return ''
            formatted_output = ''.join(
                f'?? {file}\n' for file in untracked_output)
            return formatted_output
        except subprocess.CalledProcessError as e:
            self.logger.error(
                f"Error retrieving untracked files: {e.output.decode('utf-8')}")
            return ''
