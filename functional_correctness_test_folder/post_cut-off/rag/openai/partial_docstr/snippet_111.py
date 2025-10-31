
import logging
import os
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
        self.cwd = cwd or os.getcwd()
        self.logger = logger or logging.getLogger(__name__)
        self._initial_commit: Optional[str] = None
        self._capture_initial_state()

    def _capture_initial_state(self) -> None:
        '''Capture the initial git commit hash if in a git repository.'''
        if not self.enabled:
            return
        try:
            result = subprocess.run(
                ['git', 'rev-parse', 'HEAD'],
                cwd=self.cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
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
        '''Get the current git diff from the initial state.
        Returns:
            The git diff output if enabled and there are changes, None otherwise.
        '''
        if not self.enabled or not self._initial_commit:
            return None

        cmd = [
            'git',
            'diff',
            self._initial_commit,
            '--no-color',
            '--untracked-files=all',
        ]

        # Exclude worktree paths if any
        exclusions = self._get_worktree_exclusions()
        for path in exclusions:
            # Use the :<path> syntax to exclude a path
            cmd.extend(['--', f':{path}'])

        try:
            result = subprocess.run(
                cmd,
                cwd=self.cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
            )
            diff_output = result.stdout.strip()
            if not diff_output:
                self.logger.debug("No changes detected since initial commit.")
                return None
            self.logger.debug("Diff captured with %d lines.",
                              len(diff_output.splitlines()))
            return diff_output
        except subprocess.CalledProcessError as exc:
            self.logger.error("Failed to get git diff: %s", exc.stderr.strip())
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
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
            )
            for line in result.stdout.splitlines():
                if line.startswith('worktree '):
                    # line format: worktree <path> <commit>
                    parts = line.split()
                    if len(parts) >= 2:
                        path = parts[1]
                        # Resolve to absolute path relative to repo root
                        abs_path = os.path.abspath(
                            os.path.join(self.cwd, path))
                        exclusions.append(abs_path)
            self.logger.debug("Worktree exclusions: %s", exclusions)
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
        # Use git ls-files to list untracked files
        try:
            result = subprocess.run(
                ['git', 'ls-files', '--others', '--exclude-standard'],
                cwd=self.cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
            )
            files = result.stdout.splitlines()
            # Apply exclusion patterns
            if exclude_patterns:
                filtered = []
                for f in files:
                    if any(Path(f).match(p) for p in exclude_patterns):
                        continue
                    filtered.append(f)
                files = filtered
            # Format as diff-like output
            lines = []
            for f in files:
                lines.append(f"?? {f}")
            return "\n".join(lines)
        except subprocess.CalledProcessError:
            return ""
