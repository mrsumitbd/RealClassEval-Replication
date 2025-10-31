
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
            raise ValueError("Token pool cannot be empty")
        self._tokens = list(tokens)
        self._index = 0

    def get_next_token(self) -> str:
        '''
        Get the next token in round-robin fashion.
        Returns:
            The next GitHub token to use
        '''
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
        '''Get the number of tokens in the pool.'''
        return len(self._tokens)
