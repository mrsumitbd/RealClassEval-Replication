
import logging
import subprocess
from typing import Optional


class GitDiffTracker:

    def __init__(self, enabled: bool = True, logger: Optional[logging.Logger] = None, cwd: Optional[str] = None):
        self.enabled = enabled
        self.logger = logger or logging.getLogger(__name__)
        self.cwd = cwd
        self.initial_state = None
        if enabled:
            self._capture_initial_state()

    def _capture_initial_state(self) -> None:
        try:
            self.initial_state = subprocess.check_output(
                ['git', 'status', '--porcelain'], cwd=self.cwd).decode('utf-8')
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to capture initial state: {e}")

    def get_diff(self) -> Optional[str]:
        if not self.enabled:
            return None
        try:
            current_state = subprocess.check_output(
                ['git', 'status', '--porcelain'], cwd=self.cwd).decode('utf-8')
            untracked_files = self._get_untracked_files(
                self._get_worktree_exclusions())
            diff = subprocess.check_output(['git', 'diff', '--cached'], cwd=self.cwd).decode(
                'utf-8') + untracked_files + '\n' + current_state
            if self.initial_state == current_state:
                return None
            return diff
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to get diff: {e}")
            return None

    def _get_worktree_exclusions(self) -> list[str]:
        try:
            exclusions = subprocess.check_output(
                ['git', 'ls-files', '--others', '--exclude-standard', '--directory'], cwd=self.cwd).decode('utf-8').splitlines()
            return exclusions
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to get worktree exclusions: {e}")
            return []

    def _get_untracked_files(self, exclude_patterns: list[str]) -> str:
        try:
            untracked_files = subprocess.check_output(
                ['git', 'ls-files', '--others', '--exclude-standard'], cwd=self.cwd).decode('utf-8')
            return untracked_files
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to get untracked files: {e}")
            return ''
