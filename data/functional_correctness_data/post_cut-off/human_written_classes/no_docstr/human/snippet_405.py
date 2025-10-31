from typing import Callable, Iterator
from lark.lexer import TerminalDef
import re as regex
from lark import Lark, LarkError, Token, UnexpectedInput

class LexerScope:

    def __init__(self, scope_pairs: list[tuple[regex.Pattern, regex.Pattern | Callable[[regex.Match[str]], regex.Pattern]]]=[], replace_tokens: dict[str, str | list[TerminalDef]]={}):
        self.scope_pairs = scope_pairs
        self.replace_tokens = replace_tokens

    def token_handler(self, token_stream: Iterator[Token], _scope_start_token: Token) -> Iterator[Token]:
        for t in token_stream:
            if t.type in self.replace_tokens:
                if isinstance(self.replace_tokens[t.type], str):
                    yield Token(self.replace_tokens[t.type], t.value)
                    continue
                for replace_token in self.replace_tokens[t.type]:
                    if regex.fullmatch(replace_token.pattern.to_regexp(), t.value):
                        yield Token(replace_token.name, t.value)
                        break
                else:
                    yield t
            else:
                yield t