
import logging
import os
import subprocess
from typing import Optional, List


class GitDiffTracker:

    def __init__(self, enabled: bool = True, logger: Optional[logging.Logger] = None, cwd: Optional[str] = None):
        self.enabled = enabled
        self.logger = logger
        self.cwd = cwd if cwd is not None else os.getcwd()
        self._initial_diff = None
        self._initial_untracked = None
        if self.enabled:
            self._capture_initial_state()

    def _capture_initial_state(self) -> None:
        self._initial_diff = self._get_git_diff()
        exclude_patterns = self._get_worktree_exclusions()
        self._initial_untracked = self._get_untracked_files(exclude_patterns)

    def get_diff(self) -> Optional[str]:
        if not self.enabled:
            return None

        current_diff = self._get_git_diff()
        exclude_patterns = self._get_worktree_exclusions()
        current_untracked = self._get_untracked_files(exclude_patterns)

        diff_result = ""
        if self._initial_diff != current_diff:
            diff_result += current_diff

        if self._initial_untracked != current_untracked:
            diff_result += current_untracked

        return diff_result if diff_result else None

    def _get_worktree_exclusions(self) -> List[str]:
        try:
            result = subprocess.run(
                ["git", "config", "--get-all", "core.excludesfile"],
                cwd=self.cwd,
                capture_output=True,
                text=True,
                check=True
            )
            exclude_files = result.stdout.strip().split('\n')
            patterns = []
            for file in exclude_files:
                if os.path.isfile(file):
                    with open(file, 'r') as f:
                        patterns.extend(
                            line.strip() for line in f if line.strip() and not line.startswith('#'))
            return patterns
        except subprocess.CalledProcessError:
            return []

    def _get_untracked_files(self, exclude_patterns: List[str]) -> str:
        try:
            result = subprocess.run(
                ["git", "ls-files", "--others", "--exclude-standard"],
                cwd=self.cwd,
                capture_output=True,
                text=True,
                check=True
            )
            untracked_files = result.stdout.strip().split('\n')
            filtered_files = []
            for file in untracked_files:
                if file and not any(file.startswith(pattern) for pattern in exclude_patterns):
                    filtered_files.append(file)
            return '\n'.join(filtered_files) if filtered_files else ''
        except subprocess.CalledProcessError:
            return ''

    def _get_git_diff(self) -> str:
        try:
            result = subprocess.run(
                ["git", "diff"],
                cwd=self.cwd,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError:
            return ''
