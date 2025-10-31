
import logging
import subprocess
from pathlib import Path
from typing import Optional, List


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
        self.cwd = Path(cwd) if cwd else Path.cwd()
        self.logger = logger or logging.getLogger(__name__)
        self.initial_hash: Optional[str] = None
        if self.enabled:
            self._capture_initial_state()

    def _capture_initial_state(self) -> None:
        '''Capture the initial git commit hash if in a git repository.'''
        try:
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=str(self.cwd),
                capture_output=True,
                text=True,
                check=True,
            )
            self.initial_hash = result.stdout.strip()
            self.logger.debug(
                f"Captured initial commit hash: {self.initial_hash}")
        except subprocess.CalledProcessError as exc:
            self.logger.warning(
                f"Could not capture initial commit hash: {exc}")
            self.initial_hash = None

    def get_diff(self) -> Optional[str]:
        '''Get the current git diff from the initial state.
        Returns:
            The git diff output if enabled and there are changes, None otherwise.
        '''
        if not self.enabled:
            self.logger.debug("Git diff tracking is disabled.")
            return None
        if not self.initial_hash:
            self.logger.debug(
                "No initial commit hash captured; cannot compute diff.")
            return None

        # Build git diff command
        cmd = ["git", "diff", self.initial_hash, "HEAD"]
        # Exclude worktree paths
        exclusions = self._get_worktree_exclusions()
        for pattern in exclusions:
            cmd.extend(["-x", pattern])

        try:
            diff_result = subprocess.run(
                cmd,
                cwd=str(self.cwd),
                capture_output=True,
                text=True,
                check=True,
            )
            diff_output = diff_result.stdout.strip()
        except subprocess.CalledProcessError as exc:
            self.logger.warning(f"Git diff command failed: {exc}")
            return None

        # Append untracked files
        untracked = self._get_untracked_files(exclusions)
        if untracked:
            diff_output += ("\n" if diff_output else "") + untracked

        if not diff_output:
            self.logger.debug("No changes detected since initial state.")
            return None

        self.logger.debug(f"Diff output:\n{diff_output}")
        return diff_output

    def _get_worktree_exclusions(self) -> List[str]:
        '''Get list of worktree paths to exclude from diff.
        Returns:
            List of exclusion patterns for git commands.
        '''
        exclusions: List[str] = []
        try:
            result = subprocess.run(
                ["git", "worktree", "list", "--porcelain"],
                cwd=str(self.cwd),
                capture_output=True,
                text=True,
                check=True,
            )
            for line in result.stdout.splitlines():
                if line.startswith("worktree "):
                    path = line.split(" ", 1)[1].strip()
                    # Exclude the worktree directory itself
                    exclusions.append(path)
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
        # Build git ls-files command
        cmd = ["git", "ls-files", "--others", "--exclude-standard"]
        for pattern in exclude_patterns:
            cmd.extend(["--exclude", pattern])

        try:
            result = subprocess.run(
                cmd,
                cwd=str(self.cwd),
                capture_output=True,
                text=True,
                check=True,
            )
            files = result.stdout.splitlines()
        except subprocess.CalledProcessError:
            return ""

        if not files:
            return ""

        # Format as diff-like output
        lines = [f"?? {f}" for f in files]
        return "\n".join(lines)
