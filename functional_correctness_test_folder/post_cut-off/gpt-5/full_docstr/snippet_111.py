import logging
import os
import subprocess
from pathlib import Path
from typing import Optional, List


class GitDiffTracker:
    '''Tracks git changes from an initial state through a session.'''

    EMPTY_TREE_HASH = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"

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
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s %(levelname)s %(name)s: %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

        self.cwd = Path(cwd).resolve() if cwd else Path.cwd().resolve()
        self._in_repo = False
        self._repo_root: Optional[Path] = None
        self._initial_commit: Optional[str] = None

        if self.enabled:
            self._capture_initial_state()

    def _run_git(self, args: List[str]) -> subprocess.CompletedProcess:
        try:
            return subprocess.run(
                ["git"] + args,
                cwd=str(self.cwd),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )
        except Exception as e:
            self.logger.debug("Error running git command %s: %s", args, e)
            cp = subprocess.CompletedProcess(
                ["git"] + args, returncode=1, stdout="", stderr=str(e))
            return cp

    def _capture_initial_state(self) -> None:
        '''Capture the initial git commit hash if in a git repository.'''
        if not self.enabled:
            return
        # Detect repository root
        cp = self._run_git(["rev-parse", "--show-toplevel"])
        if cp.returncode != 0:
            self._in_repo = False
            self._repo_root = None
            self._initial_commit = None
            return
        self._in_repo = True
        self._repo_root = Path(cp.stdout.strip())

        # Try to get HEAD commit; if unborn branch, fallback to empty tree
        head = self._run_git(["rev-parse", "--verify", "HEAD"])
        if head.returncode == 0:
            self._initial_commit = head.stdout.strip()
        else:
            # No commits yet
            self._initial_commit = self.EMPTY_TREE_HASH

    def get_diff(self) -> Optional[str]:
        '''Get the current git diff from the initial state.
        Returns:
            The git diff output if enabled and there are changes, None otherwise.
        '''
        if not self.enabled or not self._in_repo:
            return None

        exclude_patterns = self._get_worktree_exclusions()

        # Build pathspec exclusions
        pathspec_excludes = [f":(exclude){p}" for p in exclude_patterns if p]

        base = self._initial_commit or self.EMPTY_TREE_HASH

        # Full diff from initial commit to working tree (includes committed history and unstaged changes)
        # Use --no-color for clean output
        args = ["diff", "--no-color", base, "--"] + pathspec_excludes
        cp = self._run_git(args)
        # git diff returns 1 when differences are found in --quiet, but here stdout carries diff
        if cp.returncode not in (0, 1):
            # If the commit is not available (e.g., pruned), fallback to comparing with empty tree
            if base != self.EMPTY_TREE_HASH:
                cp = self._run_git(
                    ["diff", "--no-color", self.EMPTY_TREE_HASH, "--"] + pathspec_excludes)
            else:
                return None

        diff_output = cp.stdout

        # Append untracked files as diff-like output
        untracked = self._get_untracked_files(exclude_patterns)
        if untracked:
            if diff_output and not diff_output.endswith("\n"):
                diff_output += "\n"
            diff_output += untracked

        if not diff_output.strip():
            return None
        return diff_output

    def _get_worktree_exclusions(self) -> list[str]:
        '''Get list of worktree paths to exclude from diff.
        Returns:
            List of exclusion patterns for git commands.
        '''
        if not self._in_repo or self._repo_root is None:
            return []

        cp = self._run_git(["worktree", "list", "--porcelain"])
        if cp.returncode != 0:
            return []

        # Collect worktree paths; exclude the primary repo root
        lines = [ln.strip() for ln in cp.stdout.splitlines()]
        worktree_paths: List[Path] = []
        for ln in lines:
            if ln.startswith("worktree "):
                p = Path(ln.split(" ", 1)[1]).resolve()
                worktree_paths.append(p)

        exclusions: List[str] = []
        for wt in worktree_paths:
            if self._repo_root is not None and wt == self._repo_root:
                continue
            try:
                rel = wt.relative_to(
                    self._repo_root) if self._repo_root else None
            except ValueError:
                rel = None
            if rel:
                # Exclude the directory for this worktree
                exclusions.append(str(rel).rstrip("/"))
        # Always exclude the .git directory if pathspec supports
        exclusions.append(".git")
        return exclusions

    def _get_untracked_files(self, exclude_patterns: list[str]) -> str:
        '''Get untracked files formatted as git diff output.
        Args:
            exclude_patterns: List of patterns to exclude from the output.
        Returns:
            Formatted diff-like output for untracked files.
        '''
        if not self._in_repo:
            return ""

        cp = self._run_git(["ls-files", "--others", "--exclude-standard"])
        if cp.returncode != 0:
            return ""

        files = [ln.strip() for ln in cp.stdout.splitlines() if ln.strip()]
        if not files:
            return ""

        # Filter by exclusion patterns (simple prefix match relative to repo root)
        def excluded(path: str) -> bool:
            for pat in exclude_patterns:
                # Treat patterns as directory/file prefixes
                if pat and (path == pat or path.startswith(pat.rstrip("/") + "/")):
                    return True
            return False

        kept = [f for f in files if not excluded(f)]
        if not kept:
            return ""

        chunks: List[str] = []
        for f in kept:
            # Generate a proper diff against /dev/null to simulate a new file diff
            # Use --no-index to allow comparing filesystem paths
            file_path = str((self._repo_root / f)
                            if self._repo_root else (self.cwd / f))
            # Skip if path does not exist anymore
            if not os.path.exists(file_path):
                continue
            cp_diff = self._run_git(
                ["diff", "--no-color", "--no-index", "--", "/dev/null", file_path])
            # git diff --no-index returns 1 when differences exist; stdout contains the diff
            if cp_diff.stdout:
                # Rewrite file path to be repo-relative in headers
                # Replace absolute path with relative where possible
                out = cp_diff.stdout.replace(file_path, f)
                chunks.append(out)

        return "".join(chunks) if chunks else ""
