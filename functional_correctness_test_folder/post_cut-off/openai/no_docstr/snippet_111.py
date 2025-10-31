
import logging
import os
import subprocess
import fnmatch
from typing import Optional, List


class GitDiffTracker:
    """
    Tracks the difference between the current working tree and the state at
    the time of initialization.  It can be disabled via the `enabled`
    flag.  When enabled, the initial state is captured and subsequent
    calls to :meth:`get_diff` will return the diff between the initial
    state and the current state, including untracked files that are not
    excluded by the worktree exclusions.
    """

    def __init__(self, enabled: bool = True, logger: Optional[logging.Logger] = None, cwd: Optional[str] = None):
        """
        Parameters
        ----------
        enabled : bool, optional
            If False, the tracker will not capture any state and
            :meth:`get_diff` will always return ``None``.
        logger : logging.Logger, optional
            Logger used for debug output.  If ``None`` a default logger
            named ``GitDiffTracker`` is created.
        cwd : str, optional
            Working directory to run git commands in.  If ``None`` the
            current working directory is used.
        """
        self.enabled = enabled
        self.logger = logger or logging.getLogger("GitDiffTracker")
        self.cwd = cwd or os.getcwd()

        self._initial_diff: Optional[str] = None
        if self.enabled:
            self._capture_initial_state()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _capture_initial_state(self) -> None:
        """
        Capture the initial diff state by running ``git diff`` and
        ``git diff --cached``.  The output is stored in
        ``self._initial_diff``.  If there is no git repository or the
        commands fail, ``self._initial_diff`` is set to an empty string.
        """
        try:
            # Diff of working tree
            work_diff = subprocess.check_output(
                ["git", "diff"], cwd=self.cwd, stderr=subprocess.DEVNULL
            ).decode("utf-8", errors="ignore")

            # Diff of index (staged changes)
            index_diff = subprocess.check_output(
                ["git", "diff", "--cached"], cwd=self.cwd, stderr=subprocess.DEVNULL
            ).decode("utf-8", errors="ignore")

            # Untracked files
            untracked = self._get_untracked_files(
                self._get_worktree_exclusions())

            self._initial_diff = work_diff + index_diff + untracked
        except Exception as exc:
            self.logger.debug(f"Failed to capture initial git state: {exc}")
            self._initial_diff = ""

    def _get_worktree_exclusions(self) -> List[str]:
        """
        Return a list of patterns that should be excluded from the
        untracked files list.  The patterns are read from
        ``.git/info/exclude`` if it exists.  Each non‑empty line that
        does not start with a comment character is returned.
        """
        exclude_file = os.path.join(self.cwd, ".git", "info", "exclude")
        patterns: List[str] = []
        if os.path.isfile(exclude_file):
            try:
                with open(exclude_file, "r", encoding="utf-8") as fh:
                    for line in fh:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            patterns.append(line)
            except Exception as exc:
                self.logger.debug(f"Failed to read exclude file: {exc}")
        return patterns

    def _get_untracked_files(self, exclude_patterns: List[str]) -> str:
        """
        Return a string containing the list of untracked files, one per
        line, filtered by the given exclusion patterns.  The command
        ``git ls-files --others --exclude-standard`` is used to obtain
        the list of untracked files.  Each file is filtered against
        ``exclude_patterns`` using :func:`fnmatch.fnmatch`.
        """
        try:
            raw = subprocess.check_output(
                ["git", "ls-files", "--others", "--exclude-standard"],
                cwd=self.cwd,
                stderr=subprocess.DEVNULL,
            ).decode("utf-8", errors="ignore")
            files = [f for f in raw.splitlines() if f]
            if exclude_patterns:
                files = [
                    f
                    for f in files
                    if not any(fnmatch.fnmatch(f, pat) for pat in exclude_patterns)
                ]
            return "\n".join(files) + ("\n" if files else "")
        except Exception as exc:
            self.logger.debug(f"Failed to list untracked files: {exc}")
            return ""

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def get_diff(self) -> Optional[str]:
        """
        Return the diff between the current state and the state captured
        at initialization.  The diff includes changes in the working
        tree, staged changes, and untracked files that are not excluded.
        If there are no changes, ``None`` is returned.  If the tracker is
        disabled, ``None`` is returned.
        """
        if not self.enabled:
            return None

        try:
            # Current diffs
            work_diff = subprocess.check_output(
                ["git", "diff"], cwd=self.cwd, stderr=subprocess.DEVNULL
            ).decode("utf-8", errors="ignore")

            index_diff = subprocess.check_output(
                ["git", "diff", "--cached"], cwd=self.cwd, stderr=subprocess.DEVNULL
            ).decode("utf-8", errors="ignore")

            untracked = self._get_untracked_files(
                self._get_worktree_exclusions())

            current_diff = work_diff + index_diff + untracked

            # If nothing changed since initial capture, return None
            if current_diff == self._initial_diff:
                return None

            return current_diff
        except Exception as exc:
            self.logger.debug(f"Failed to get git diff: {exc}")
            return None
