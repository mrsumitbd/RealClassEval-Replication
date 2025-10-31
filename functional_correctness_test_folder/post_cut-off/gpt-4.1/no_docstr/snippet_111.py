
import logging
import subprocess
from typing import Optional, List


class GitDiffTracker:

    def __init__(self, enabled: bool = True, logger: Optional[logging.Logger] = None, cwd: Optional[str] = None):
        self.enabled = enabled
        self.logger = logger or logging.getLogger(__name__)
        self.cwd = cwd
        self._initial_diff = None
        self._initial_untracked = None
        if self.enabled:
            self._capture_initial_state()

    def _capture_initial_state(self) -> None:
        self._initial_diff = self._run_git(['diff', '--no-ext-diff'])
        exclusions = self._get_worktree_exclusions()
        self._initial_untracked = self._get_untracked_files(exclusions)

    def get_diff(self) -> Optional[str]:
        if not self.enabled:
            return None
        current_diff = self._run_git(['diff', '--no-ext-diff'])
        exclusions = self._get_worktree_exclusions()
        current_untracked = self._get_untracked_files(exclusions)
        diff_parts = []
        if current_diff != self._initial_diff:
            diff_parts.append('--- Modified files diff ---\n' + current_diff)
        if current_untracked != self._initial_untracked:
            diff_parts.append('--- Untracked files ---\n' + current_untracked)
        if diff_parts:
            return '\n\n'.join(diff_parts)
        return None

    def _get_worktree_exclusions(self) -> list[str]:
        try:
            output = self._run_git(
                ['ls-files', '--exclude-standard', '-oi', '--directory'])
            patterns = []
            for line in output.splitlines():
                if line.endswith('/'):
                    patterns.append(line)
            return patterns
        except Exception:
            return []

    def _get_untracked_files(self, exclude_patterns: list[str]) -> str:
        args = ['ls-files', '--exclude-standard', '-o']
        if exclude_patterns:
            for pat in exclude_patterns:
                args.extend(['--exclude', pat])
        return self._run_git(args)

    def _run_git(self, args: List[str]) -> str:
        try:
            result = subprocess.run(
                ['git'] + args,
                cwd=self.cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            self.logger.error(
                f"Git command failed: {' '.join(args)}\n{e.stderr}")
            return ""
