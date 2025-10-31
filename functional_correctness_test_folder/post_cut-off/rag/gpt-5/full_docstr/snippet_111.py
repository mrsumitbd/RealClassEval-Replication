import logging
import os
import shutil
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
        self.logger = logger or logging.getLogger(__name__)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s %(levelname)s %(name)s: %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

        self.cwd = cwd or os.getcwd()
        self.enabled = bool(enabled)
        self.git_path = shutil.which('git')
        self.inside_work_tree = False
        self.repo_root: Optional[str] = None
        self.initial_commit: Optional[str] = None
        self.exclude_patterns: List[str] = []

        if not self.enabled:
            return
        if not self.git_path:
            self.logger.debug('git not found on PATH; disabling diff tracking')
            self.enabled = False
            return

        self._capture_initial_state()

    def _run_git(self, args: List[str], cwd: Optional[str] = None) -> subprocess.CompletedProcess:
        cmd = [self.git_path or 'git'] + args
        try:
            cp = subprocess.run(
                cmd,
                cwd=cwd or self.cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return cp
        except Exception as exc:
            self.logger.debug(
                'Failed to run git command %s: %s', ' '.join(cmd), exc)
            # Create a faux CompletedProcess with error
            return subprocess.CompletedProcess(cmd, returncode=255, stdout='', stderr=str(exc))

    def _capture_initial_state(self) -> None:
        '''Capture the initial git commit hash if in a git repository.'''
        cp = self._run_git(['rev-parse', '--is-inside-work-tree'])
        if cp.returncode != 0 or cp.stdout.strip().lower() != 'true':
            self.enabled = False
            self.logger.debug(
                'Not inside a git work tree; disabling diff tracking')
            return

        self.inside_work_tree = True

        cp_root = self._run_git(['rev-parse', '--show-toplevel'])
        if cp_root.returncode == 0:
            self.repo_root = cp_root.stdout.strip()
        else:
            # Fallback to current working directory
            self.repo_root = self.cwd

        cp_head = self._run_git(['rev-parse', '--verify', 'HEAD'])
        if cp_head.returncode == 0:
            self.initial_commit = cp_head.stdout.strip()
        else:
            self.initial_commit = None  # Repository may have no commits yet

        self.exclude_patterns = self._get_worktree_exclusions()

    def get_diff(self) -> Optional[str]:
        '''Get the current git diff from the initial state.
        Returns:
            The git diff output if enabled and there are changes, None otherwise.
        '''
        if not self.enabled or not self.inside_work_tree:
            return None

        args = ['diff']
        if self.initial_commit:
            args.append(self.initial_commit)

        # Ensure we include the whole tree, then apply excludes.
        # Git pathspec requires at least one positive path; '.' selects all files.
        pathspec = ['--', '.']
        pathspec.extend(self.exclude_patterns)
        args.extend(pathspec)

        cp = self._run_git(args, cwd=self.repo_root)
        if cp.returncode not in (0, 1):
            self.logger.debug('git diff failed (rc=%s): %s',
                              cp.returncode, cp.stderr.strip())
            return None

        diff_output = cp.stdout

        # Append untracked files as diff-like patches
        untracked = self._get_untracked_files(self.exclude_patterns)
        combined = diff_output
        if untracked:
            if combined and not combined.endswith('\n'):
                combined += '\n'
            combined += untracked

        combined = combined.strip('\n')
        if not combined:
            return None
        return combined

    def _get_worktree_exclusions(self) -> list[str]:
        '''Get list of worktree paths to exclude from diff.
        Returns:
            List of exclusion patterns for git commands.
        '''
        # We will attempt to exclude additional worktrees if they are nested
        # within this repo root. Normally, additional worktrees are outside
        # and do not affect the current worktree.
        if not self.inside_work_tree or not self.repo_root:
            return []

        cp = self._run_git(
            ['worktree', 'list', '--porcelain'], cwd=self.repo_root)
        if cp.returncode != 0:
            return []

        excludes: List[str] = []
        current_root = os.path.normpath(self.repo_root)

        for line in cp.stdout.splitlines():
            line = line.strip()
            if not line or not line.startswith('worktree '):
                continue
            path = line.split(' ', 1)[1].strip()
            norm = os.path.normpath(path)
            # Create a relative path if it's within current repo root
            try:
                rel = os.path.relpath(norm, start=current_root)
            except Exception:
                rel = norm
            if not rel.startswith('..') and rel != '.':
                # Exclude the other worktree path only if nested (rare)
                excludes.append(f':(exclude){rel}')

        # Deduplicate while preserving order
        seen = set()
        result: List[str] = []
        for pat in excludes:
            if pat not in seen:
                seen.add(pat)
                result.append(pat)

        return result

    def _get_untracked_files(self, exclude_patterns: list[str]) -> str:
        '''Get untracked files formatted as git diff output.
        Args:
            exclude_patterns: List of patterns to exclude from the output.
        Returns:
            Formatted diff-like output for untracked files.
        '''
        if not self.inside_work_tree or not self.repo_root:
            return ''

        # Collect untracked files
        cp = self._run_git(
            ['ls-files', '--others', '--exclude-standard', '-z'], cwd=self.repo_root)
        if cp.returncode != 0:
            self.logger.debug(
                'git ls-files for untracked failed (rc=%s): %s', cp.returncode, cp.stderr.strip())
            return ''

        raw = cp.stdout
        if not raw:
            return ''

        files = [p for p in raw.split('\x00') if p]
        if not files:
            return ''

        # Build a simple exclusion based on provided pathspec excludes of the form ':(exclude)path'
        exclude_paths: List[str] = []
        for pat in exclude_patterns:
            if pat.startswith(':(exclude)'):
                exclude_paths.append(pat[len(':(exclude)'):].lstrip('/'))

        def is_excluded(relpath: str) -> bool:
            rp = relpath.replace('\\', '/')
            for ex in exclude_paths:
                exn = ex.replace('\\', '/').rstrip('/')
                if rp == exn or rp.startswith(exn + '/'):
                    return True
            return False

        diffs: List[str] = []
        for rel in files:
            if is_excluded(rel):
                continue
            # Generate patch for untracked file with --no-index against /dev/null
            # This returns rc=1 when differences exist (i.e., always for new file)
            cp_patch = self._run_git(
                ['diff', '--no-index', '--', '/dev/null', rel], cwd=self.repo_root)
            if cp_patch.returncode in (0, 1) and cp_patch.stdout:
                diffs.append(cp_patch.stdout)

        return ''.join(diffs)
