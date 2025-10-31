
import logging
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
        self.cwd = cwd if cwd else '.'
        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(logging.INFO)
        self.initial_state = None
        if enabled:
            self._capture_initial_state()

    def _capture_initial_state(self) -> None:
        try:
            self.initial_state = subprocess.check_output(
                ['git', 'status', '--porcelain'], cwd=self.cwd).decode('utf-8')
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to capture initial git state: {e}")
            self.enabled = False

    def get_diff(self) -> Optional[str]:
        '''Get the current git diff from the initial state.
        Returns:
            The git diff output if enabled and there are changes, None otherwise.
        '''
        if not self.enabled:
            return None
        try:
            current_state = subprocess.check_output(
                ['git', 'status', '--porcelain'], cwd=self.cwd).decode('utf-8')
            if current_state == self.initial_state:
                return None
            exclude_patterns = self._get_worktree_exclusions()
            diff_output = subprocess.check_output(['git', 'diff', '--cached'] + [
                                                  f'--exclude={pattern}' for pattern in exclude_patterns], cwd=self.cwd).decode('utf-8')
            untracked_files = self._get_untracked_files(exclude_patterns)
            if untracked_files:
                diff_output += '\n' + untracked_files
            return diff_output.strip() or None
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to get git diff: {e}")
            return None

    def _get_worktree_exclusions(self) -> list[str]:
        '''Get list of worktree paths to exclude from diff.
        Returns:
            List of exclusion patterns for git commands.
        '''
        try:
            worktree_paths = subprocess.check_output(
                ['git', 'worktree', 'list', '--porcelain'], cwd=self.cwd).decode('utf-8').splitlines()
            exclusions = []
            for line in worktree_paths:
                if line.startswith('path '):
                    path = line.split(' ', 1)[1]
                    exclusions.append(path)
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
        try:
            untracked_files = subprocess.check_output(['git', 'ls-files', '--others', '--exclude-standard'] + [
                                                      f'--exclude={pattern}' for pattern in exclude_patterns], cwd=self.cwd).decode('utf-8').splitlines()
            output = []
            for file in untracked_files:
                with open(file, 'r') as f:
                    file_contents = f.read()
                output.append(
                    f'diff --git a/{file} b/{file}\nnew file mode 100644\nindex 0000000..{hash(file_contents.encode("utf-8"))}\n--- /dev/null\n+++ b/{file}\n@@ -0,0 +1 @@\n+{file_contents}')
            return '\n'.join(output)
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to get untracked files: {e}")
            return ''
