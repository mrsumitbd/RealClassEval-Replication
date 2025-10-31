
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
        self.initial_commit_hash = None
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
            self.initial_commit_hash = result.stdout.strip()
        except subprocess.CalledProcessError as e:
            self.logger.warning(f"Failed to capture initial git state: {e}")
            self.enabled = False

    def get_diff(self) -> Optional[str]:
        '''Get the current git diff from the initial state.
        Returns:
            The git diff output if enabled and there are changes, None otherwise.
        '''
        if not self.enabled or self.initial_commit_hash is None:
            return None

        try:
            exclude_patterns = self._get_worktree_exclusions()
            diff_cmd = ['git', 'diff', '--no-ext-diff', '--unified=0',
                        '--no-color', '--no-prefix', self.initial_commit_hash]
            diff_cmd.extend(['--'] + exclude_patterns)
            diff_result = subprocess.run(
                diff_cmd,
                cwd=self.cwd,
                capture_output=True,
                text=True,
                check=True
            )
            untracked_files = self._get_untracked_files(exclude_patterns)
            diff_output = diff_result.stdout + untracked_files
            return diff_output if diff_output.strip() else None
        except subprocess.CalledProcessError as e:
            self.logger.warning(f"Failed to get git diff: {e}")
            return None

    def _get_worktree_exclusions(self) -> list[str]:
        '''Get list of worktree paths to exclude from diff.
        Returns:
            List of exclusion patterns for git commands.
        '''
        try:
            result = subprocess.run(
                ['git', 'config', '--get-regexp', 'diff\.gitDiffTracker\.exclude'],
                cwd=self.cwd,
                capture_output=True,
                text=True,
                check=True
            )
            exclusions = [line.split()[1]
                          for line in result.stdout.strip().split('\n') if line.strip()]
            return exclusions
        except subprocess.CalledProcessError as e:
            self.logger.warning(f"Failed to get worktree exclusions: {e}")
            return []

    def _get_untracked_files(self, exclude_patterns: list[str]) -> str:
        '''Get untracked files formatted as git diff output.
        Args:
            exclude_patterns: List of patterns to exclude from the output.
        Returns:
            Formatted diff-like output for untracked files.
        '''
        try:
            ls_files_cmd = ['git', 'ls-files', '--others',
                            '--exclude-standard', '--full-name']
            ls_files_cmd.extend(['--'] + exclude_patterns)
            result = subprocess.run(
                ls_files_cmd,
                cwd=self.cwd,
                capture_output=True,
                text=True,
                check=True
            )
            untracked_files = result.stdout.strip().split('\n')
            if not untracked_files or untracked_files == ['']:
                return ''

            diff_output = []
            for file in untracked_files:
                if not file.strip():
                    continue
                diff_output.append(f"diff --git a/{file} b/{file}")
                diff_output.append("new file mode 100644")
                diff_output.append("index 0000000..")
                with open(os.path.join(self.cwd, file), 'r') as f:
                    content = f.read()
                diff_output.append(f"--- /dev/null")
                diff_output.append(f"+++ b/{file}")
                diff_output.append("@@ -0,0 +1 @@")
                for line in content.split('\n'):
                    diff_output.append(f"+{line}")
            return '\n'.join(diff_output) + '\n'
        except subprocess.CalledProcessError as e:
            self.logger.warning(f"Failed to get untracked files: {e}")
            return ''
