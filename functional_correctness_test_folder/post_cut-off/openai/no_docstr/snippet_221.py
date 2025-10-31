
from typing import List


class GitHubTokenPool:
    def __init__(self, tokens: List[str]):
        if not tokens:
            raise ValueError("Token list cannot be empty")
        self._tokens = list(tokens)
        self._index = 0

    def get_next_token(self) -> str:
        """Return the next token in the pool and advance the pointer."""
        token = self._tokens[self._index]
        self._index = (self._index + 1) % len(self._tokens)
        return token

    def get_current_token(self) -> str:
        """Return the current token without advancing the pointer."""
        return self._tokens[self._index]

    @property
    def pool_size(self) -> int:
        """Return the number of tokens in the pool."""
        return len(self._tokens)
