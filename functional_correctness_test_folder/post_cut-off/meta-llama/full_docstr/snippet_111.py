
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
        self.initial_commit_hash = None
        if not logger:
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(logging.INFO)
        else:
            self.logger = logger
        if enabled:
            self._capture_initial_state()

    def _capture_initial_state(self) -> None:
        '''Capture the initial git commit hash if in a git repository.'''
        try:
            self.initial_commit_hash = subprocess.check_output(
                ['git', 'rev-parse', 'HEAD'], cwd=self.cwd).decode('utf-8').strip()
        except subprocess.CalledProcessError:
            self.logger.warning(
                'Not a git repository, git diff tracking disabled.')
            self.enabled = False

    def get_diff(self) -> Optional[str]:
        '''Get the current git diff from the initial state.
        Returns:
            The git diff output if enabled and there are changes, None otherwise.
        '''
        if not self.enabled:
            return None
        try:
            diff_output = subprocess.check_output(
                ['git', 'diff', self.initial_commit_hash, '--'] + self._get_worktree_exclusions(), cwd=self.cwd).decode('utf-8')
            untracked_files = self._get_untracked_files(
                self._get_worktree_exclusions())
            if diff_output or untracked_files:
                return diff_output + untracked_files
            else:
                return None
        except subprocess.CalledProcessError as e:
            self.logger.error(f'Failed to get git diff: {e}')
            return None

    def _get_worktree_exclusions(self) -> list[str]:
        '''Get list of worktree paths to exclude from diff.
        Returns:
            List of exclusion patterns for git commands.
        '''
        try:
            exclusions = subprocess.check_output(
                ['git', 'ls-files', '--others', '--exclude-standard', '--directory'], cwd=self.cwd).decode('utf-8').splitlines()
            exclusions = [f':!{exclusion}' for exclusion in exclusions]
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
            untracked_files = subprocess.check_output(
                ['git', 'ls-files', '--others', '--exclude-standard'] + exclude_patterns, cwd=self.cwd).decode('utf-8').splitlines()
            diff_output = ''
            for file in untracked_files:
                diff_output += f'diff --git a/{file} b/{file}\n'
                diff_output += f'new file mode 100644\n'
                diff_output += f'index 0000000..{self._get_file_hash(file)}\n'
                diff_output += f'--- /dev/null\n'
                diff_output += f'+++ b/{file}\n'
                with open(f'{self.cwd}/{file}', 'r') as f:
                    for line in f.readlines():
                        diff_output += f'+{line}'
            return diff_output
        except subprocess.CalledProcessError:
            return ''

    def _get_file_hash(self, file: str) -> str:
        '''Get the hash of a file.
        Args:
            file: Path to the file.
        Returns:
            Hash of the file.
        '''
        try:
            return subprocess.check_output(['git', 'hash-object', file], cwd=self.cwd).decode('utf-8').strip()
        except subprocess.CalledProcessError:
            return '0000000'
