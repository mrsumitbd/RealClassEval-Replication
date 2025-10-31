
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
        self.initial_commit = None
        self.in_git_repo = False
        if self.enabled:
            self._capture_initial_state()

    def _capture_initial_state(self) -> None:
        '''Capture the initial git commit hash if in a git repository.'''
        try:
            result = subprocess.run(
                ['git', 'rev-parse', 'HEAD'],
                cwd=self.cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            self.initial_commit = result.stdout.strip()
            self.in_git_repo = True
            self.logger.debug(f"Initial commit hash: {self.initial_commit}")
        except subprocess.CalledProcessError:
            self.in_git_repo = False
            self.initial_commit = None
            self.logger.info(
                "Not a git repository or unable to get initial commit hash.")

    def get_diff(self) -> Optional[str]:
        '''Get the current git diff from the initial state.
        Returns:
            The git diff output if enabled and there are changes, None otherwise.
        '''
        if not self.enabled or not self.in_git_repo or not self.initial_commit:
            return None

        exclusions = self._get_worktree_exclusions()
        diff_cmd = ['git', 'diff', self.initial_commit, '--']
        for pattern in exclusions:
            diff_cmd.extend(['":(exclude)"' + pattern])

        try:
            # Run git diff
            result = subprocess.run(
                diff_cmd,
                cwd=self.cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=False
            )
            diff_output = result.stdout
        except Exception as e:
            self.logger.error(f"Error running git diff: {e}")
            return None

        # Get untracked files
        untracked = self._get_untracked_files(exclusions)

        # Combine outputs if any
        combined = ''
        if diff_output.strip():
            combined += diff_output
        if untracked.strip():
            if combined:
                combined += '\n'
            combined += untracked

        return combined if combined.strip() else None

    def _get_worktree_exclusions(self) -> List[str]:
        '''Get list of worktree paths to exclude from diff.
        Returns:
            List of exclusion patterns for git commands.
        '''
        # Example: Exclude .git, .venv, __pycache__, etc.
        exclusions = ['.git', '.venv', 'venv', '__pycache__']
        # Add more patterns as needed
        return exclusions

    def _get_untracked_files(self, exclude_patterns: List[str]) -> str:
        '''Get untracked files formatted as git diff output.
        Args:
            exclude_patterns: List of patterns to exclude from the output.
        Returns:
            Formatted diff-like output for untracked files.
        '''
        cmd = ['git', 'ls-files', '--others', '--exclude-standard']
        try:
            result = subprocess.run(
                cmd,
                cwd=self.cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=False
            )
            files = result.stdout.strip().splitlines()
        except Exception as e:
            self.logger.error(f"Error running git ls-files: {e}")
            return ''

        # Filter out excluded patterns
        filtered = []
        for f in files:
            if any(f.startswith(pattern) or f.split(os.sep)[0] == pattern for pattern in exclude_patterns):
                continue
            filtered.append(f)

        if not filtered:
            return ''

        # Format as diff-like output
        output = []
        for f in filtered:
            output.append(f"diff --git a/{f} b/{f}")
            output.append(f"new file mode 100644")
            output.append(f"--- /dev/null")
            output.append(f"+++ b/{f}")
            try:
                with open(os.path.join(self.cwd, f), 'r', encoding='utf-8', errors='replace') as file:
                    lines = file.readlines()
                output.append(f"@@ 0,0 1,{len(lines)} @@")
                for line in lines:
                    output.append(f"+{line.rstrip()}")
            except Exception as e:
                output.append(f"+[Could not read file: {e}]")
        return '\n'.join(output)
