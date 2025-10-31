
import logging
import os
import subprocess
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
        self.cwd = cwd or os.getcwd()
        if logger is not None:
            self.logger = logger
        else:
            self.logger = logging.getLogger(__name__)
            if not self.logger.hasHandlers():
                handler = logging.StreamHandler()
                formatter = logging.Formatter(
                    '%(asctime)s %(levelname)s %(message)s')
                handler.setFormatter(formatter)
                self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
        self._initial_tree = None
        self._initial_untracked = None
        if self.enabled:
            self._capture_initial_state()

    def _capture_initial_state(self) -> None:
        try:
            self._initial_tree = subprocess.check_output(
                ['git', 'rev-parse', 'HEAD'],
                cwd=self.cwd,
                stderr=subprocess.DEVNULL
            ).decode().strip()
        except Exception:
            self._initial_tree = None
        try:
            exclude_patterns = self._get_worktree_exclusions()
            self._initial_untracked = set(
                self._get_untracked_file_list(exclude_patterns))
        except Exception:
            self._initial_untracked = set()

    def get_diff(self) -> Optional[str]:
        '''Get the current git diff from the initial state.
        Returns:
            The git diff output if enabled and there are changes, None otherwise.
        '''
        if not self.enabled or self._initial_tree is None:
            return None
        exclude_patterns = self._get_worktree_exclusions()
        try:
            # Get diff for tracked files
            diff_cmd = ['git', 'diff', self._initial_tree]
            for pat in exclude_patterns:
                diff_cmd.extend(['--', f':(exclude){pat}'])
            diff = subprocess.check_output(
                diff_cmd,
                cwd=self.cwd
            ).decode()
        except Exception as e:
            self.logger.warning(f"Failed to get git diff: {e}")
            diff = ""
        # Get diff for untracked files
        try:
            untracked_diff = self._get_untracked_files(exclude_patterns)
        except Exception as e:
            self.logger.warning(f"Failed to get untracked files diff: {e}")
            untracked_diff = ""
        result = (diff + untracked_diff).strip()
        return result if result else None

    def _get_worktree_exclusions(self) -> List[str]:
        '''Get list of worktree paths to exclude from diff.
        Returns:
            List of exclusion patterns for git commands.
        '''
        # Exclude .git directory and possibly other common patterns
        return ['.git']

    def _get_untracked_file_list(self, exclude_patterns: List[str]) -> List[str]:
        cmd = ['git', 'ls-files', '--others', '--exclude-standard']
        for pat in exclude_patterns:
            cmd.extend(['--', f':(exclude){pat}'])
        try:
            output = subprocess.check_output(cmd, cwd=self.cwd).decode()
            files = [line.strip()
                     for line in output.splitlines() if line.strip()]
            return files
        except Exception:
            return []

    def _get_untracked_files(self, exclude_patterns: list[str]) -> str:
        '''Get untracked files formatted as git diff output.
        Args:
            exclude_patterns: List of patterns to exclude from the output.
        Returns:
            Formatted diff-like output for untracked files.
        '''
        current_untracked = set(
            self._get_untracked_file_list(exclude_patterns))
        initial_untracked = self._initial_untracked or set()
        new_untracked = current_untracked - initial_untracked
        diffs = []
        for file in sorted(new_untracked):
            file_path = os.path.join(self.cwd, file)
            if not os.path.isfile(file_path):
                continue
            try:
                with open(file_path, 'rb') as f:
                    content = f.read()
                try:
                    content_str = content.decode('utf-8')
                except UnicodeDecodeError:
                    content_str = content.decode('latin1')
                diff = (
                    f"diff --git a/{file} b/{file}\n"
                    f"new file mode 100644\n"
                    f"--- /dev/null\n"
                    f"+++ b/{file}\n"
                    f"@@ -0,0 +1,{len(content_str.splitlines())} @@\n"
                )
                for line in content_str.splitlines():
                    diff += f"+{line}\n"
                diffs.append(diff)
            except Exception as e:
                self.logger.warning(
                    f"Could not read untracked file {file}: {e}")
        return ''.join(diffs)
