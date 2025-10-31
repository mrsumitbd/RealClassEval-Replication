
import logging
import os
import subprocess
from typing import Optional, List


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
        self.cwd = cwd or os.getcwd()
        self._initial_commit_hash = None
        if self.enabled:
            self._capture_initial_state()

    def _capture_initial_state(self) -> None:
        """Capture the initial git commit hash if in a git repository."""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', 'HEAD'],
                cwd=self.cwd,
                capture_output=True,
                text=True,
                check=True
            )
            self._initial_commit_hash = result.stdout.strip()
        except subprocess.CalledProcessError:
            self.logger.debug(
                "Not in a git repository, diff tracking disabled")
            self.enabled = False
        except Exception as e:
            self.logger.warning(f"Failed to capture initial git state: {e}")
            self.enabled = False

    def get_diff(self) -> Optional[str]:
        """Get the current git diff from the initial state.
        Returns:
            The git diff output if enabled and there are changes, None otherwise.
        """
        if not self.enabled or not self._initial_commit_hash:
            return None

        try:
            exclude_patterns = self._get_worktree_exclusions()
            diff_output = subprocess.run(
                ['git', 'diff', self._initial_commit_hash],
                cwd=self.cwd,
                capture_output=True,
                text=True,
                check=True
            ).stdout

            untracked_output = self._get_untracked_files(exclude_patterns)
            if diff_output or untracked_output:
                return (diff_output + untracked_output).strip() or None
            return None
        except subprocess.CalledProcessError as e:
            self.logger.warning(f"Failed to get git diff: {e}")
            return None
        except Exception as e:
            self.logger.warning(f"Unexpected error getting git diff: {e}")
            return None

    def _get_worktree_exclusions(self) -> list[str]:
        """Get list of worktree paths to exclude from diff.
        Returns:
            List of exclusion patterns for git commands.
        """
        try:
            result = subprocess.run(
                ['git', 'config', '--get-all', 'core.excludesfile'],
                cwd=self.cwd,
                capture_output=True,
                text=True,
                check=False
            )
            exclude_files = result.stdout.splitlines()
            return [f":(exclude){f.strip()}" for f in exclude_files if f.strip()]
        except Exception:
            return []

    def _get_untracked_files(self, exclude_patterns: list[str]) -> str:
        """Get untracked files formatted as git diff output.
        Args:
            exclude_patterns: List of patterns to exclude from the output.
        Returns:
            Formatted diff-like output for untracked files.
        """
        try:
            untracked = subprocess.run(
                ['git', 'ls-files', '--others',
                    '--exclude-standard'] + exclude_patterns,
                cwd=self.cwd,
                capture_output=True,
                text=True,
                check=True
            ).stdout.splitlines()

            if not untracked:
                return ""

            output = []
            for file in untracked:
                output.append(f"diff --git a/{file} b/{file}")
                output.append(f"new file mode 100644")
                output.append(f"index {'0'*40}..{'0'*40}")
                output.append(f"--- /dev/null")
                output.append(f"+++ b/{file}")
            return "\n".join(output) + "\n"
        except subprocess.CalledProcessError as e:
            self.logger.warning(f"Failed to get untracked files: {e}")
            return ""
        except Exception as e:
            self.logger.warning(
                f"Unexpected error getting untracked files: {e}")
            return ""
