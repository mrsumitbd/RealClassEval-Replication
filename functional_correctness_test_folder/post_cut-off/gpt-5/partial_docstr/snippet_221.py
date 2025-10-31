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
        if not isinstance(tokens, list):
            raise TypeError("tokens must be a list of strings")
        if not tokens:
            raise ValueError("tokens list cannot be empty")
        if any(not isinstance(t, str) or not t for t in tokens):
            raise ValueError("all tokens must be non-empty strings")
        self._tokens: List[str] = tokens[:]
        self._index: int = 0
        self._lock = threading.Lock()

    def get_next_token(self) -> str:
        with self._lock:
            self._index = (self._index + 1) % len(self._tokens)
            return self._tokens[self._index]

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
        return len(self._tokens)
