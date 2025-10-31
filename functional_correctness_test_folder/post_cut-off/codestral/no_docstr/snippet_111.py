
import logging
import os
import subprocess
from typing import Optional


class GitDiffTracker:

    def __init__(self, enabled: bool = True, logger: Optional[logging.Logger] = None, cwd: Optional[str] = None):
        self.enabled = enabled
        self.logger = logger or logging.getLogger(__name__)
        self.cwd = cwd or os.getcwd()
        self.initial_state = None

    def _capture_initial_state(self) -> None:
        if not self.enabled:
            return

        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.cwd,
                capture_output=True,
                text=True,
                check=True
            )
            self.initial_state = result.stdout
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to capture initial state: {e}")
            self.initial_state = None

    def get_diff(self) -> Optional[str]:
        if not self.enabled or self.initial_state is None:
            return None

        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.cwd,
                capture_output=True,
                text=True,
                check=True
            )
            current_state = result.stdout

            if current_state == self.initial_state:
                return None

            result = subprocess.run(
                ["git", "diff", "--no-ext-diff", "--no-color", "--no-textconv"],
                cwd=self.cwd,
                capture_output=True,
                text=True,
                check=True
            )
            diff = result.stdout

            untracked_files = self._get_untracked_files(
                self._get_worktree_exclusions())
            if untracked_files:
                diff += f"\nUntracked files:\n{untracked_files}"

            return diff
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to get diff: {e}")
            return None

    def _get_worktree_exclusions(self) -> list[str]:
        exclusions = []
        try:
            result = subprocess.run(
                ["git", "config", "--get-regexp",
                    "^diff\\.gitmodules\\..*\\.worktree"],
                cwd=self.cwd,
                capture_output=True,
                text=True,
                check=True
            )
            for line in result.stdout.splitlines():
                _, value = line.split(maxsplit=1)
                exclusions.append(value)
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to get worktree exclusions: {e}")
        return exclusions

    def _get_untracked_files(self, exclude_patterns: list[str]) -> str:
        untracked_files = ""
        try:
            result = subprocess.run(
                ["git", "ls-files", "--others", "--exclude-standard"],
                cwd=self.cwd,
                capture_output=True,
                text=True,
                check=True
            )
            for pattern in exclude_patterns:
                result = subprocess.run(
                    ["git", "check-ignore", "--no-index", "-v", pattern],
                    cwd=self.cwd,
                    capture_output=True,
                    text=True,
                    check=True
                )
                if result.stdout:
                    continue
                result = subprocess.run(
                    ["git", "ls-files", "--others", "--exclude-standard", pattern],
                    cwd=self.cwd,
                    capture_output=True,
                    text=True,
                    check=True
                )
                untracked_files += result.stdout
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to get untracked files: {e}")
        return untracked_files
