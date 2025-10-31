from typing import Optional
import subprocess
import os
import logging
import time

class GitDiffTracker:
    """Tracks git changes from an initial state through a session."""

    def __init__(self, enabled: bool=True, logger: Optional[logging.Logger]=None, cwd: Optional[str]=None):
        """Initialize the git diff tracker.

        Args:
            enabled: Whether to enable git diff tracking (default: True)
            logger: Optional logger instance to use for logging. If not provided,
                    creates a default logger for this module.
            cwd: Working directory for git commands (default: current directory)
        """
        self.enabled = enabled
        self.cwd = cwd
        self.initial_git_hash: Optional[str] = None
        self.session_start_time = time.time()
        self.logger = logger or logging.getLogger(__name__)
        if self.enabled:
            self._capture_initial_state()

    def _capture_initial_state(self) -> None:
        """Capture the initial git commit hash if in a git repository."""
        try:
            result = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True, timeout=5, cwd=self.cwd)
            if result.returncode == 0 and result.stdout.strip():
                self.initial_git_hash = result.stdout.strip()
                self.logger.info(f'Git diff tracking enabled. Initial commit: {self.initial_git_hash[:8]}')
            else:
                self.enabled = False
                self.logger.info('Not in a git repository or no commits found. Git diff tracking disabled.')
        except subprocess.TimeoutExpired:
            self.enabled = False
            self.logger.warning('Git command timed out. Git diff tracking disabled.')
        except Exception as e:
            self.enabled = False
            self.logger.warning(f'Failed to initialize git tracking: {e}')

    def get_diff(self) -> Optional[str]:
        """Get the current git diff from the initial state.

        Returns:
            The git diff output if enabled and there are changes, None otherwise.
        """
        if not self.enabled:
            return None
        try:
            combined_output = ''
            exclude_patterns = self._get_worktree_exclusions()
            if self.initial_git_hash:
                diff_cmd = ['git', 'diff', self.initial_git_hash]
            else:
                diff_cmd = ['git', 'diff', 'HEAD']
            if exclude_patterns:
                diff_cmd.extend(['--'] + exclude_patterns)
            result = subprocess.run(diff_cmd, capture_output=True, text=True, timeout=5, cwd=self.cwd)
            if result.returncode == 0 and result.stdout.strip():
                combined_output = result.stdout.strip()
            untracked_output = self._get_untracked_files(exclude_patterns)
            if untracked_output:
                if combined_output:
                    combined_output += '\n'
                combined_output += untracked_output
            return combined_output
        except subprocess.TimeoutExpired:
            self.logger.warning('Git diff command timed out')
            return None
        except Exception as e:
            self.logger.warning(f'Failed to get git diff: {e}')
            return None

    def _get_worktree_exclusions(self) -> list[str]:
        """Get list of worktree paths to exclude from diff.

        Returns:
            List of exclusion patterns for git commands.
        """
        exclude_patterns = []
        try:
            worktree_result = subprocess.run(['git', 'worktree', 'list', '--porcelain'], capture_output=True, text=True, timeout=5, cwd=self.cwd)
            if worktree_result.returncode == 0:
                current_dir = self.cwd or os.getcwd()
                for line in worktree_result.stdout.strip().split('\n'):
                    if line.startswith('worktree '):
                        worktree_path = line[9:]
                        if worktree_path != current_dir and worktree_path.startswith(os.path.dirname(current_dir)):
                            try:
                                rel_path = os.path.relpath(worktree_path, current_dir)
                                if not rel_path.startswith('..'):
                                    exclude_patterns.append(f':(exclude){rel_path}')
                            except ValueError:
                                pass
        except Exception:
            pass
        return exclude_patterns

    def _get_untracked_files(self, exclude_patterns: list[str]) -> str:
        """Get untracked files formatted as git diff output.

        Args:
            exclude_patterns: List of patterns to exclude from the output.

        Returns:
            Formatted diff-like output for untracked files.
        """
        output = ''
        try:
            untracked_cmd = ['git', 'ls-files', '--others', '--exclude-standard']
            if exclude_patterns:
                untracked_cmd.extend(['--'] + exclude_patterns)
            result = subprocess.run(untracked_cmd, capture_output=True, text=True, timeout=5, cwd=self.cwd)
            if result.returncode == 0 and result.stdout.strip():
                untracked_files = result.stdout.strip().split('\n')
                for file_path in untracked_files:
                    try:
                        abs_file_path = os.path.join(self.cwd or os.getcwd(), file_path)
                        file_creation_time = os.path.getctime(abs_file_path)
                        if file_creation_time < self.session_start_time:
                            continue
                    except (OSError, IOError):
                        continue
                    output += f'diff --git a/{file_path} b/{file_path}\n'
                    output += 'new file mode 100644\n'
                    output += 'index 0000000..0000000\n'
                    output += '--- /dev/null\n'
                    output += f'+++ b/{file_path}\n'
                    try:
                        with open(abs_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = f.readlines()
                            output += f'@@ -0,0 +1,{len(lines)} @@\n'
                            for line in lines:
                                if line.endswith('\n'):
                                    output += f'+{line}'
                                else:
                                    output += f'+{line}\n'
                            if lines and (not lines[-1].endswith('\n')):
                                output += '\n\\ No newline at end of file\n'
                    except Exception:
                        output += '@@ -0,0 +1,1 @@\n'
                        output += '+[Binary or unreadable file]\n'
                    output += '\n'
        except Exception:
            pass
        return output