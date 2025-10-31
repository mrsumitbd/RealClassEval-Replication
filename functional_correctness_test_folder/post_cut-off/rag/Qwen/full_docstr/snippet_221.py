
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
        self.tokens = tokens
        self.current_index = 0

    def get_next_token(self) -> str:
        '''
        Get the next token in round-robin fashion.
        Returns:
            The next GitHub token to use
        '''
        if not self.tokens:
            raise ValueError("No tokens available in the pool.")
        token = self.tokens[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.tokens)
        return token

    def get_current_token(self) -> str:
        '''
        Get the current token without advancing the index.
        Returns:
            The current GitHub token
        '''
        if not self.tokens:
            raise ValueError("No tokens available in the pool.")
        return self.tokens[self.current_index]

    @property
    def pool_size(self) -> int:
        '''Get the number of tokens in the pool.'''
        return len(self.tokens)
