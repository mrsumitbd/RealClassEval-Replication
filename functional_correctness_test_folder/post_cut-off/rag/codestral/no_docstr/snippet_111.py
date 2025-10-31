
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
        if not self.enabled or self.initial_commit is None:
            return None

        try:
            # Get the diff from initial commit to current state
            diff_cmd = ['git', 'diff', self.initial_commit, '--']
            diff_result = subprocess.run(
                diff_cmd,
                cwd=self.cwd,
                capture_output=True,
                text=True,
                check=True
            )

            # Get untracked files
            untracked_files = self._get_untracked_files(
                self._get_worktree_exclusions())

            # Combine both diffs
            combined_diff = diff_result.stdout
            if untracked_files:
                combined_diff += "\n" + untracked_files

            return combined_diff if combined_diff.strip() else None
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to get git diff: {e.stderr}")
            return None

    def _get_worktree_exclusions(self) -> list[str]:
        '''Get list of worktree paths to exclude from diff.
        Returns:
            List of exclusion patterns for git commands.
        '''
        exclusions = []
        try:
            result = subprocess.run(
                ['git', 'config', '--get-regexp', 'diff\.gitdiff\.exclude'],
                cwd=self.cwd,
                capture_output=True,
                text=True,
                check=True
            )
            for line in result.stdout.splitlines():
                if line.strip():
                    _, pattern = line.split(maxsplit=1)
                    exclusions.append(pattern)
        except subprocess.CalledProcessError:
            pass
        return exclusions

    def _get_untracked_files(self, exclude_patterns: list[str]) -> str:
        '''Get untracked files formatted as git diff output.
        Args:
            exclude_patterns: List of patterns to exclude from the output.
        Returns:
            Formatted diff-like output for untracked files.
        '''
        try:
            # Get untracked files
            untracked_cmd = ['git', 'ls-files',
                             '--others', '--exclude-standard']
            for pattern in exclude_patterns:
                untracked_cmd.extend(['--exclude', pattern])

            untracked_result = subprocess.run(
                untracked_cmd,
                cwd=self.cwd,
                capture_output=True,
                text=True,
                check=True
            )

            if not untracked_result.stdout.strip():
                return ""

            # Format untracked files as diff output
            diff_output = "diff --git a/untracked b/untracked\n"
            diff_output += "new file mode 100644\n"
            diff_output += "index 0000000..0000000\n"
            diff_output += "--- /dev/null\n"
            diff_output += "+++ b/untracked\n"
            diff_output += "@@ -0,0 +1 @@\n"
            diff_output += "+" + \
                "\n+".join(untracked_result.stdout.splitlines())

            return diff_output
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to get untracked files: {e.stderr}")
            return ""
