
from typing import List


class GitHubTokenPool:
    '''
    Manages a pool of GitHub tokens with round-robin selection.
    '''

    def __init__(self, tokens: List[str]):
        '''
        Initialize token pool.
        Args:
            tokens: List of GitHub personal access tokens
        '''
        if not tokens:
            raise ValueError("Token list must not be empty.")
        self._tokens = tokens[:]
        self._index = 0

    def get_next_token(self) -> str:
        token = self._tokens[self._index]
        self._index = (self._index + 1) % len(self._tokens)
        return token

    def get_current_token(self) -> str:
        '''
        Get the current token without advancing the index.
        Returns:
            The current GitHub token
        '''
        return self._tokens[self._index]

    @property
    def pool_size(self) -> int:
        return len(self._tokens)
