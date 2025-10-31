from typing import List
from threading import Lock


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
        if tokens is None:
            raise ValueError("tokens cannot be None")
        if not isinstance(tokens, list):
            raise TypeError("tokens must be a list of strings")
        cleaned = []
        for t in tokens:
            if not isinstance(t, str):
                raise TypeError("all tokens must be strings")
            st = t.strip()
            if not st:
                raise ValueError("tokens must not be empty or whitespace")
            cleaned.append(st)
        if not cleaned:
            raise ValueError("token pool cannot be empty")
        self._tokens = tuple(cleaned)
        self._index = 0
        self._lock = Lock()

    def get_next_token(self) -> str:
        '''
        Get the next token in round-robin fashion.
        Returns:
            The next GitHub token to use
        '''
        with self._lock:
            token = self._tokens[self._index]
            self._index = (self._index + 1) % len(self._tokens)
            return token

    def get_current_token(self) -> str:
        '''
        Get the current token without advancing the index.
        Returns:
            The current GitHub token
        '''
        with self._lock:
            return self._tokens[self._index]

    @property
    def pool_size(self) -> int:
        '''Get the number of tokens in the pool.'''
        return len(self._tokens)
