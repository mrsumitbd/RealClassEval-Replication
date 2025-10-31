
import logging
import os
import subprocess
from typing import Optional


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
            result = subprocess.run(
                ['git', 'rev-parse', 'HEAD'],
                cwd=self.cwd,
                capture_output=True,
                text=True,
                check=True
            )
            self.initial_commit = result.stdout.strip()
        except subprocess.CalledProcessError:
            self.logger.warning(
                "Not in a git repository or git command failed")
            self.enabled = False

    def get_diff(self) -> Optional[str]:
        '''Get the current git diff from the initial state.
        Returns:
            The git diff output if enabled and there are changes, None otherwise.
        '''
        if not self.enabled or not self.initial_commit:
            return None

        try:
            # Get the diff from initial commit to current state
            diff_cmd = ['git', 'diff', self.initial_commit, '--']
            exclude_patterns = self._get_worktree_exclusions()
            if exclude_patterns:
                diff_cmd.extend(['--'] + exclude_patterns)

            diff_result = subprocess.run(
                diff_cmd,
                cwd=self.cwd,
                capture_output=True,
                text=True,
                check=True
            )

            # Get untracked files
            untracked_diff = self._get_untracked_files(exclude_patterns)

            # Combine both diffs
            combined_diff = diff_result.stdout
            if untracked_diff:
                combined_diff += untracked_diff

            return combined_diff if combined_diff.strip() else None
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to get git diff: {e}")
            return None

    def _get_worktree_exclusions(self) -> list[str]:
        '''Get list of worktree paths to exclude from diff.
        Returns:
            List of exclusion patterns for git commands.
        '''
        try:
            result = subprocess.run(
                ['git', 'worktree', 'list', '--porcelain'],
                cwd=self.cwd,
                capture_output=True,
                text=True,
                check=True
            )
            exclusions = []
            for line in result.stdout.splitlines():
                if line.startswith('worktree '):
                    path = line.split()[1]
                    exclusions.append(f':(exclude){path}')
            return exclusions
        except subprocess.CalledProcessError:
            return []

    def _get_untracked_files(self, exclude_patterns: list[str]) -> str:
        '''Get untracked files formatted as git diff output.
        Args:
            exclude_patterns: List of patterns to exclude from the output.
        Returns:
            Formatted diff-like output for untracked files.
        '''
        try:
            ls_files_cmd = ['git', 'ls-files',
                            '--others', '--exclude-standard']
            if exclude_patterns:
                ls_files_cmd.extend(exclude_patterns)

            result = subprocess.run(
                ls_files_cmd,
                cwd=self.cwd,
                capture_output=True,
                text=True,
                check=True
            )

            untracked_files = result.stdout.strip().splitlines()
            if not untracked_files:
                return ""

            diff_output = "diff --git a/ /dev/null\n"
            diff_output += "new file mode 100644\n"
            diff_output += "index 0000000..\n"
            diff_output += "---\n"
            diff_output += "+++ b/\n"

            for file in untracked_files:
                diff_output += f"\nUntracked file: {file}\n"

            return diff_output
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to get untracked files: {e}")
            return ""
