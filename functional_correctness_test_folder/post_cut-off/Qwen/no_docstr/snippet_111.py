
import logging
import os
import subprocess
from typing import Optional, List


class GitDiffTracker:

    def __init__(self, enabled: bool = True, logger: Optional[logging.Logger] = None, cwd: Optional[str] = None):
        self.enabled = enabled
        self.logger = logger
        self.cwd = cwd if cwd else os.getcwd()
        if self.enabled:
            self._capture_initial_state()

    def _capture_initial_state(self) -> None:
        try:
            self.initial_commit = subprocess.check_output(
                ['git', 'rev-parse', 'HEAD'], cwd=self.cwd).strip().decode('utf-8')
        except subprocess.CalledProcessError:
            if self.logger:
                self.logger.error("Failed to capture initial commit state.")
            self.initial_commit = None

    def get_diff(self) -> Optional[str]:
        if not self.enabled or self.initial_commit is None:
            return None
        try:
            diff = subprocess.check_output(
                ['git', 'diff', self.initial_commit], cwd=self.cwd).decode('utf-8')
            return diff if diff else None
        except subprocess.CalledProcessError:
            if self.logger:
                self.logger.error("Failed to get diff.")
            return None

    def _get_worktree_exclusions(self) -> List[str]:
        try:
            exclude_patterns = subprocess.check_output(
                ['git', 'config', '--get', 'core.excludesFile'], cwd=self.cwd).strip().decode('utf-8')
            with open(exclude_patterns, 'r') as file:
                return [line.strip() for line in file if line.strip() and not line.startswith('#')]
        except (subprocess.CalledProcessError, FileNotFoundError):
            if self.logger:
                self.logger.error("Failed to get worktree exclusions.")
            return []

    def _get_untracked_files(self, exclude_patterns: List[str]) -> str:
        try:
            untracked_files = subprocess.check_output(
                ['git', 'ls-files', '--others', '--exclude-from=-'], cwd=self.cwd, input='\n'.join(exclude_patterns).encode('utf-8')).decode('utf-8')
            return untracked_files
        except subprocess.CalledProcessError:
            if self.logger:
                self.logger.error("Failed to get untracked files.")
            return ''
