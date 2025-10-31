
from typing import List


class GitHubTokenPool:

    def __init__(self, tokens: List[str]):
        self.tokens = tokens
        self.current_index = 0

    def get_next_token(self) -> str:
        if not self.tokens:
            raise ValueError("Token pool is empty")
        token = self.tokens[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.tokens)
        return token

    def get_current_token(self) -> str:
        if not self.tokens:
            raise ValueError("Token pool is empty")
        return self.tokens[self.current_index]

    @property
    def pool_size(self) -> int:
        return len(self.tokens)
