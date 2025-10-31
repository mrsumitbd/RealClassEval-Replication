from typing import List
import threading


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
            raise ValueError("tokens must not be None")
        cleaned = [t.strip()
                   for t in tokens if isinstance(t, str) and t.strip()]
        if not cleaned:
            raise ValueError(
                "tokens must contain at least one non-empty string")
        self._tokens = tuple(cleaned)
        self._index = 0
        self._lock = threading.Lock()

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
