
import logging
import subprocess
from pathlib import Path
from typing import List, Optional


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
        self.cwd = cwd or Path.cwd()
        self.logger = logger or logging.getLogger(__name__)
        self._initial_hash: Optional[str] = None
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
                check=True,
            )
            self._initial_hash = result.stdout.strip()
            self.logger.debug(
                f'Initial git hash captured: {self._initial_hash}')
        except subprocess.CalledProcessError:
            self._initial_hash = None
            self.logger.debug(
                'Not a git repository or HEAD not found; diff tracking disabled.')

    def get_diff(self) -> Optional[str]:
        '''Get the current git diff from the initial state.
        Returns:
            The git diff output if enabled and there are changes, None otherwise.
        '''
        if not self.enabled or not self._initial_hash:
            return None

        # Get diff between initial commit and current HEAD
        try:
            diff_result = subprocess.run(
                ['git', 'diff', self._initial_hash, 'HEAD'],
                cwd=self.cwd,
                capture_output=True,
                text=True,
                check=True,
            )
            diff_output = diff_result.stdout
        except subprocess.CalledProcessError as exc:
            self.logger.error(f'git diff failed: {exc}')
            diff_output = ''

        # Get untracked files
        exclusions = self._get_worktree_exclusions()
        untracked_output = self._get_untracked_files(exclusions)

        # Combine outputs
        combined = diff_output + untracked_output
        if combined.strip():
            return combined
        return None

    def _get_worktree_exclusions(self) -> List[str]:
        '''Get list of worktree paths to exclude from diff.
        Returns:
            List of exclusion patterns for git commands.
        '''
        exclusions: List[str] = []
        try:
            result = subprocess.run(
                ['git', 'worktree', 'list', '--porcelain'],
                cwd=self.cwd,
                capture_output=True,
                text=True,
                check=True,
            )
            for line in result.stdout.splitlines():
                if line.startswith('worktree '):
                    parts = line.split()
                    if len(parts) >= 2:
                        path = parts[1]
                        # Convert relative path to absolute
                        abs_path = (Path(self.cwd) / path).resolve()
                        exclusions.append(str(abs_path))
        except subprocess.CalledProcessError:
            # No worktrees or git not available; ignore
            pass
        return exclusions

    def _get_untracked_files(self, exclude_patterns: List[str]) -> str:
        '''Get untracked files formatted as git diff output.
        Args:
            exclude_patterns: List of patterns to exclude from the output.
        Returns:
            Formatted diff-like output for untracked files.
        '''
        cmd = ['git', 'ls-files', '--others', '--exclude-standard']
        for pattern in exclude_patterns:
            cmd.extend(['--exclude', pattern])
        try:
            result = subprocess.run(
                cmd,
                cwd=self.cwd,
                capture_output=True,
                text=True,
                check=True,
            )
            files = result.stdout.splitlines()
            # Format as diff-like: "?? <file>"
            formatted = '\n'.join(f'?? {f}' for f in files)
            if formatted:
                formatted += '\n'
            return formatted
        except subprocess.CalledProcessError:
            return ''
