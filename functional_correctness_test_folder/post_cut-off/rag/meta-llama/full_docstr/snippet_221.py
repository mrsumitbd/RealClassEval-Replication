
from typing import List


class GitHubTokenPool:
    """
    Manages a pool of GitHub tokens with round-robin selection.
    """

    def __init__(self, tokens: List[str]):
        """
        Initialize token pool.

        Args:
            tokens: List of GitHub personal access tokens
        """
        self.tokens = tokens
        self.index = 0

    def get_next_token(self) -> str:
        """
        Get the next token in round-robin fashion.

        Returns:
            The next GitHub token to use
        """
        token = self.tokens[self.index]
        self.index = (self.index + 1) % len(self.tokens)
        return token

    def get_current_token(self) -> str:
        """
        Get the current token without advancing the index.

        Returns:
            The current GitHub token
        """
        return self.tokens[self.index]

    @property
    def pool_size(self) -> int:
        """
        Get the number of tokens in the pool.

        Returns:
            The number of tokens in the pool
        """
        return len(self.tokens)
