from typing import Any, Callable, ClassVar, Dict, Generic, Iterable, List, Match, MutableMapping, Optional, Pattern, Type, TypeVar, Union, cast

class InlineState:
    """The state to save inline parser's tokens."""

    def __init__(self, env: MutableMapping[str, Any]):
        self.env = env
        self.src = ''
        self.tokens: List[Dict[str, Any]] = []
        self.in_image = False
        self.in_link = False
        self.in_emphasis = False
        self.in_strong = False

    def prepend_token(self, token: Dict[str, Any]) -> None:
        """Insert token before the last token."""
        self.tokens.insert(len(self.tokens) - 1, token)

    def append_token(self, token: Dict[str, Any]) -> None:
        """Add token to the end of token list."""
        self.tokens.append(token)

    def copy(self) -> 'InlineState':
        """Create a copy of current state."""
        state = self.__class__(self.env)
        state.in_image = self.in_image
        state.in_link = self.in_link
        state.in_emphasis = self.in_emphasis
        state.in_strong = self.in_strong
        return state