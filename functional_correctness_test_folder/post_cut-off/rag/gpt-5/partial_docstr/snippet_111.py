import logging
import os
import subprocess
from typing import Optional, List


class GitDiffTracker:
    '''Tracks git changes from an initial state through a session.'''

    EMPTY_TREE_HASH = '4b825dc642cb6eb9a060e54bf8d69288fbee4904'

    def __init__(self, enabled: bool = True, logger: Optional[logging.Logger] = None, cwd: Optional[str] = None):
        '''Initialize the git diff tracker.
        Args:
            enabled: Whether to enable git diff tracking (default: True)
            logger: Optional logger instance to use for logging. If not provided,
                    creates a default logger for this module.
            cwd: Working directory for git commands (default: current directory)
        '''
        self.enabled = bool(enabled)
        self.logger = logger or logging.getLogger(__name__)
        self.cwd = cwd or os.getcwd()
        self.initial_hash: Optional[str] = None
        self._in_repo = False

        if self.enabled:
            self._capture_initial_state()

    def _run_git(self, args: List[str], allow_nonzero: bool = False) -> tuple[bool, str, str]:
        try:
            cp = subprocess.run(
                ['git', *args],
                cwd=self.cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                errors='replace',
                check=False,
            )
        except FileNotFoundError:
            self.logger.debug(
                'git executable not found; disabling git diff tracking')
            return False, '', 'git not found'
        ok = (cp.returncode == 0) or allow_nonzero
        return ok, cp.stdout, cp.stderr

    def _capture_initial_state(self) -> None:
        '''Capture the initial git commit hash if in a git repository.'''
        ok, out, _ = self._run_git(['rev-parse', '--is-inside-work-tree'])
        if not ok or out.strip().lower() != 'true':
            self._in_repo = False
            self.initial_hash = None
            return

        self._in_repo = True
        ok, out, _ = self._run_git(['rev-parse', '--verify', 'HEAD'])
        if ok:
            self.initial_hash = out.strip()
        else:
            # Repository without commits; use empty tree as baseline.
            self.initial_hash = self.EMPTY_TREE_HASH

    def get_diff(self) -> Optional[str]:
        '''Get the current git diff from the initial state.
        Returns:
            The git diff output if enabled and there are changes, None otherwise.
        '''
        if not self.enabled or not self._in_repo or not self.initial_hash:
            return None

        exclude_patterns = self._get_worktree_exclusions()
        pathspec = ['--', '.'] + [f':(exclude){p}' for p in exclude_patterns]

        # git diff may return non-zero (1) when there are differences; that's expected.
        ok, diff_out, err = self._run_git(
            ['diff', '--no-ext-diff', '--binary',
                '--no-color', self.initial_hash, *pathspec],
            allow_nonzero=True,
        )
        if not ok and not diff_out:
            # Some unexpected error occurred
            self.logger.debug('git diff failed: %s', err.strip())
            return None

        untracked_out = self._get_untracked_files(exclude_patterns)
        combined = (diff_out or '') + (untracked_out or '')

        return combined if combined.strip() else None

    def _get_worktree_exclusions(self) -> list[str]:
        '''Get list of worktree paths to exclude from diff.
        Returns:
            List of exclusion patterns for git commands.
        '''
        ok, top_out, _ = self._run_git(['rev-parse', '--show-toplevel'])
        if not ok:
            return []

        toplevel = os.path.abspath(top_out.strip())
        ok, wt_out, _ = self._run_git(['worktree', 'list', '--porcelain'])
        if not ok or not wt_out.strip():
            return []

        exclusions: list[str] = []
        for line in wt_out.splitlines():
            line = line.strip()
            if not line.startswith('worktree '):
                continue
            wt_path = line.split(' ', 1)[1].strip()
            wt_abs = os.path.abspath(wt_path)
            if wt_abs == toplevel:
                continue
            # Only exclude subpaths that are inside the current toplevel
            if wt_abs.startswith(toplevel + os.sep):
                rel = os.path.relpath(wt_abs, toplevel)
                rel = rel.replace(os.sep, '/')
                exclusions.append(rel)
        return exclusions

    def _get_untracked_files(self, exclude_patterns: list[str]) -> str:
        '''Get untracked files formatted as git diff output.
        Args:
            exclude_patterns: List of patterns to exclude from the output.
        Returns:
            Formatted diff-like output for untracked files.
        '''
        # List untracked files using porcelain and standard ignores
        ok, out, err = self._run_git(
            ['ls-files', '--others', '--exclude-standard', '-z'])
        if not ok and not out:
            self.logger.debug('git ls-files failed: %s', err.strip())
            return ''

        entries = [p for p in out.split('\x00') if p]
        if not entries:
            return ''

        def is_excluded(path: str) -> bool:
            path_posix = path.replace(os.sep, '/')
            for pat in exclude_patterns:
                if path_posix == pat or path_posix.startswith(pat.rstrip('/') + '/'):
                    return True
            return False

        # Build diffs for each untracked file as "diff --no-index /dev/null <file>"
        diffs: list[str] = []
        for p in entries:
            if is_excluded(p):
                continue
            # Skip directories (ls-files should list files only, but be safe)
            abs_p = os.path.join(self.cwd, p)
            if os.path.isdir(abs_p):
                continue
            # Use -- to avoid ambiguity, allow non-zero exit (differences produce code 1)
            ok, d_out, _ = self._run_git(
                ['diff', '--no-index', '--binary', '--no-color', '--', '/dev/null', p], allow_nonzero=True)
            if d_out:
                diffs.append(d_out)

        return ''.join(diffs) if diffs else ''
