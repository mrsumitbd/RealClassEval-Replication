
from typing import List


class GitHubTokenPool:

    def __init__(self, tokens: List[str]):
        if not tokens:
            raise ValueError("Token list cannot be empty.")
        self._tokens = tokens[:]
        self._index = 0

    def get_next_token(self) -> str:
        self._index = (self._index + 1) % len(self._tokens)
        return self._tokens[self._index]

    def get_current_token(self) -> str:
        return self._tokens[self._index]

    @property
    def pool_size(self) -> int:
        return len(self._tokens)
