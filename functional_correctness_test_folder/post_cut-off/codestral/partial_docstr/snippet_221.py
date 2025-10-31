
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
        Get the next token in the pool, advancing the index.
        Returns:
            The next GitHub token
        '''
        token = self.tokens[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.tokens)
        return token

    def get_current_token(self) -> str:
        '''
        Get the current token without advancing the index.
        Returns:
            The current GitHub token
        '''
        return self.tokens[self.current_index]

    @property
    def pool_size(self) -> int:
        '''
        Get the size of the token pool.
        Returns:
            The number of tokens in the pool
        '''
        return len(self.tokens)
