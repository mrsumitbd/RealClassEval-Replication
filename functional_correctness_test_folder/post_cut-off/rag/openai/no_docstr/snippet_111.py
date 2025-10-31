
import logging
import os
import subprocess
from pathlib import Path
from typing import List, Optional


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
        self.cwd = cwd or os.getcwd()
        self.logger = logger or logging.getLogger(__name__)
        self._initial_commit: Optional[str] = None
        self._capture_initial_state()

    def _capture_initial_state(self) -> None:
        """Capture the initial git commit hash if in a git repository."""
        if not self.enabled:
            return
        try:
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=self.cwd,
                capture_output=True,
                text=True,
                check=True,
            )
            self._initial_commit = result.stdout.strip()
            self.logger.debug("Captured initial commit: %s",
                              self._initial_commit)
        except (subprocess.CalledProcessError, FileNotFoundError):
            self._initial_commit = None
            self.logger.debug(
                "Not a git repository or git not available; diff tracking disabled.")

    def get_diff(self) -> Optional[str]:
        """Get the current git diff from the initial state.

        Returns:
            The git diff output if enabled and there are changes, None otherwise.
        """
        if not self.enabled or not self._initial_commit:
            return None

        # Get diff between initial commit and current HEAD
        try:
            diff_result = subprocess.run(
                ["git", "diff", self._initial_commit, "HEAD"],
                cwd=self.cwd,
                capture_output=True,
                text=True,
                check=True,
            )
            diff_output = diff_result.stdout
        except subprocess.CalledProcessError as exc:
            self.logger.error("git diff failed: %s", exc)
            return None

        # Get untracked files
        exclusions = self._get_worktree_exclusions()
        untracked = self._get_untracked_files(exclusions)

        # Combine diff and untracked
        combined = diff_output
        if untracked:
            if combined and not combined.endswith("\n"):
                combined += "\n"
            combined += untracked

        if not combined.strip():
            return None
        return combined

    def _get_worktree_exclusions(self) -> List[str]:
        """Get list of worktree paths to exclude from diff.

        Returns:
            List of exclusion patterns for git commands.
        """
        exclusions: List[str] = []
        try:
            result = subprocess.run(
                ["git", "worktree", "list", "--porcelain"],
                cwd=self.cwd,
                capture_output=True,
                text=True,
                check=True,
            )
            for line in result.stdout.splitlines():
                if line.startswith("worktree "):
                    path = line.split(" ", 1)[1]
                    # Exclude the worktree directory itself
                    exclusions.append(path)
        except subprocess.CalledProcessError:
            # No worktrees or git not available
            pass
        return exclusions

    def _get_untracked_files(self, exclude_patterns: List[str]) -> str:
        """Get untracked files formatted as git diff output.

        Args:
            exclude_patterns: List of patterns to exclude from the output.

        Returns:
            Formatted diff-like output for untracked files.
        """
        try:
            result = subprocess.run(
                ["git", "ls-files", "--others", "--exclude-standard"],
                cwd=self.cwd,
                capture_output=True,
                text=True,
                check=True,
            )
            files = result.stdout.splitlines()
        except subprocess.CalledProcessError:
            return ""

        # Filter out excluded worktree paths
        def is_excluded(path: str) -> bool:
            for pattern in exclude_patterns:
                if Path(path).match(pattern):
                    return True
            return False

        filtered = [f for f in files if not is_excluded(f)]

        if not filtered:
            return ""

        # Build a simple diff-like representation
        parts: List[str] = []
        for f in filtered:
            parts.append(f"?? {f}")
        return "\n".join(parts) + "\n"
