
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
        self.initial_state = None
        if self.enabled:
            self._capture_initial_state()

    def _capture_initial_state(self) -> None:
        if not self.enabled:
            return
        try:
            result = subprocess.run(
                ['git', 'rev-parse', '--show-toplevel'],
                cwd=self.cwd,
                capture_output=True,
                text=True,
                check=True
            )
            repo_root = result.stdout.strip()
            result = subprocess.run(
                ['git', 'ls-files', '-z'],
                cwd=repo_root,
                capture_output=True,
                text=True,
                check=True
            )
            tracked_files = result.stdout.split('\0')
            result = subprocess.run(
                ['git', 'diff', '--cached', '--name-only', '-z'],
                cwd=repo_root,
                capture_output=True,
                text=True,
                check=True
            )
            staged_files = result.stdout.split('\0')
            result = subprocess.run(
                ['git', 'diff', '--name-only', '-z'],
                cwd=repo_root,
                capture_output=True,
                text=True,
                check=True
            )
            unstaged_files = result.stdout.split('\0')
            self.initial_state = {
                'repo_root': repo_root,
                'tracked_files': tracked_files,
                'staged_files': staged_files,
                'unstaged_files': unstaged_files
            }
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to capture initial git state: {e}")
            self.enabled = False

    def get_diff(self) -> Optional[str]:
        '''Get the current git diff from the initial state.
        Returns:
            The git diff output if enabled and there are changes, None otherwise.
        '''
        if not self.enabled or not self.initial_state:
            return None
        try:
            repo_root = self.initial_state['repo_root']
            exclude_patterns = self._get_worktree_exclusions()
            result = subprocess.run(
                ['git', 'diff', '--cached'] + exclude_patterns,
                cwd=repo_root,
                capture_output=True,
                text=True,
                check=True
            )
            staged_diff = result.stdout
            result = subprocess.run(
                ['git', 'diff'] + exclude_patterns,
                cwd=repo_root,
                capture_output=True,
                text=True,
                check=True
            )
            unstaged_diff = result.stdout
            untracked_diff = self._get_untracked_files(exclude_patterns)
            combined_diff = staged_diff + unstaged_diff + untracked_diff
            if combined_diff.strip():
                return combined_diff
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to get git diff: {e}")
        return None

    def _get_worktree_exclusions(self) -> list[str]:
        '''Get list of worktree paths to exclude from diff.
        Returns:
            List of exclusion patterns for git commands.
        '''
        if not self.enabled or not self.initial_state:
            return []
        try:
            repo_root = self.initial_state['repo_root']
            result = subprocess.run(
                ['git', 'worktree', 'list', '--porcelain'],
                cwd=repo_root,
                capture_output=True,
                text=True,
                check=True
            )
            worktrees = result.stdout.split('\n')
            exclusions = []
            for line in worktrees:
                if line.startswith('worktree '):
                    path = line.split()[1]
                    exclusions.append(f':(exclude){path}')
            return exclusions
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to get worktree exclusions: {e}")
            return []

    def _get_untracked_files(self, exclude_patterns: list[str]) -> str:
        '''Get untracked files formatted as git diff output.
        Args:
            exclude_patterns: List of patterns to exclude from the output.
        Returns:
            Formatted diff-like output for untracked files.
        '''
        if not self.enabled or not self.initial_state:
            return ''
        try:
            repo_root = self.initial_state['repo_root']
            result = subprocess.run(
                ['git', 'ls-files', '--others',
                    '--exclude-standard', '-z'] + exclude_patterns,
                cwd=repo_root,
                capture_output=True,
                text=True,
                check=True
            )
            untracked_files = result.stdout.split('\0')
            diff_output = ''
            for file in untracked_files:
                if file:
                    diff_output += f'diff --git a/{file} b/{file}\n'
                    diff_output += 'new file mode 100644\n'
                    diff_output += 'index 0000000..\n'
                    diff_output += '--- /dev/null\n'
                    diff_output += f'+++ b/{file}\n'
                    with open(os.path.join(repo_root, file), 'r') as f:
                        content = f.read()
                    diff_output += f'@@ -0,0 +1 @@\n{content}\n'
            return diff_output
        except (subprocess.CalledProcessError, IOError) as e:
            self.logger.error(f"Failed to get untracked files: {e}")
            return ''
