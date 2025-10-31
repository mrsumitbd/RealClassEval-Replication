
import logging
import subprocess
from typing import Optional


class GitDiffTracker:
    """Tracks git changes from an initial state through a session."""

    def __init__(self, enabled: bool = True, logger: Optional[logging.Logger] = None, cwd: Optional[str] = None):
        """Initialize the git diff tracker.

        Args:
            enabled: Whether to enable git diff tracking (default: True)
            logger: Optional logger instance to use for logging. If not provided,
                    creates a default logger for this module.
            cwd: Working directory for git commands (default: current directory)
        """
        self.enabled = enabled
        self.logger = logger or logging.getLogger(__name__)
        self.cwd = cwd or '.'
        self.initial_commit_hash = None
        if enabled:
            self._capture_initial_state()

    def _capture_initial_state(self) -> None:
        """Capture the initial git commit hash if in a git repository."""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', 'HEAD'], cwd=self.cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                self.initial_commit_hash = result.stdout.strip().decode('utf-8')
        except FileNotFoundError:
            self.logger.warning(
                'Git executable not found. Git diff tracking disabled.')
            self.enabled = False

    def get_diff(self) -> Optional[str]:
        """Get the current git diff from the initial state.

        Returns:
            The git diff output if enabled and there are changes, None otherwise.
        """
        if not self.enabled or self.initial_commit_hash is None:
            return None

        try:
            exclude_patterns = self._get_worktree_exclusions()
            untracked_files = self._get_untracked_files(exclude_patterns)
            diff_command = ['git', 'diff', self.initial_commit_hash]
            for pattern in exclude_patterns:
                diff_command.extend(['--', f':(exclude){pattern}'])
            result = subprocess.run(
                diff_command, cwd=self.cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                diff_output = result.stdout.decode('utf-8')
                if untracked_files:
                    diff_output += '\n' + untracked_files
                return diff_output.strip() or None
            else:
                self.logger.error('Failed to get git diff: %s',
                                  result.stderr.decode('utf-8'))
        except Exception as e:
            self.logger.error('Error getting git diff: %s', e)

        return None

    def _get_worktree_exclusions(self) -> list[str]:
        """Get list of worktree paths to exclude from diff.

        Returns:
            List of exclusion patterns for git commands.
        """
        try:
            result = subprocess.run(['git', 'worktree', 'list', '--porcelain'],
                                    cwd=self.cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                worktree_paths = [line.split()[1] for line in result.stdout.decode(
                    'utf-8').splitlines() if line.startswith('worktree')]
                return worktree_paths
        except Exception as e:
            self.logger.error('Error getting worktree exclusions: %s', e)
        return []

    def _get_untracked_files(self, exclude_patterns: list[str]) -> str:
        """Get untracked files formatted as git diff output.

        Args:
            exclude_patterns: List of patterns to exclude from the output.

        Returns:
            Formatted diff-like output for untracked files.
        """
        try:
            ls_files_command = ['git', 'ls-files',
                                '--others', '--exclude-standard']
            for pattern in exclude_patterns:
                ls_files_command.extend(['--exclude', pattern])
            result = subprocess.run(
                ls_files_command, cwd=self.cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                untracked_files = result.stdout.decode('utf-8').splitlines()
                if untracked_files:
                    diff_output = ''
                    for file in untracked_files:
                        with open(file, 'r') as f:
                            file_content = f.read()
                        diff_output += f'diff --git a/{file} b/{file}\nnew file mode 100644\nindex 0000000..{file.replace("/", "")}\n--- /dev/null\n+++ b/{file}\n@@ -0,0 +1 @@\n+{file_content}\n'
                    return diff_output
        except Exception as e:
            self.logger.error('Error getting untracked files: %s', e)
        return ''
