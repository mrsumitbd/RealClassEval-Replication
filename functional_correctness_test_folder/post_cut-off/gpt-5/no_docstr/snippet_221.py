from typing import List
import threading


class GitHubTokenPool:
    def __init__(self, tokens: List[str]):
        if not isinstance(tokens, list):
            raise TypeError("tokens must be a list of strings")
        cleaned = []
        for t in tokens:
            if not isinstance(t, str):
                raise TypeError("all tokens must be strings")
            s = t.strip()
            if not s:
                continue
            cleaned.append(s)
        if not cleaned:
            raise ValueError(
                "tokens list must contain at least one non-empty string")
        self._tokens = tuple(cleaned)
        self._index = -1
        self._lock = threading.Lock()

    def get_next_token(self) -> str:
        with self._lock:
            self._index = (self._index + 1) % len(self._tokens)
            return self._tokens[self._index]

    def get_current_token(self) -> str:
        with self._lock:
            if self._index == -1:
                return self._tokens[0]
            return self._tokens[self._index]

    @property
    def pool_size(self) -> int:
        return len(self._tokens)
