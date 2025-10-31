from loguru import logger
from contextlib import contextmanager

class FeatureBranch:

    def __init__(self, name: str, git_repo: 'GitRepository'):
        self.name = name
        self._git_repo = git_repo
        self.repo_dir = git_repo.repo_dir

    def commit_all(self, commit_msg: str) -> None:
        logger.info(f"Committing all changes from '{self.name}'...")
        self._git_repo.checkout_branch(self.name)
        self._git_repo.commit_all(commit_msg)
        logger.info('Committed all changes.')

    def push_to_remote(self) -> None:
        logger.info(f"Pushing to remote: '{self.name}'...")
        self._git_repo.push_to_remote(self.name)
        logger.success(f"Pushed changes to remote: '{self.name}'")

    @contextmanager
    def create_changes(self, commit_msg: str):
        """Context manager to create changes in the feature branch."""
        try:
            self._git_repo.checkout_branch(self.name)
            yield self
            self.commit_all(commit_msg)
            self.push_to_remote()
        except Exception as e:
            logger.error(f"Failed to create changes in '{self.name}': {e}")
            raise