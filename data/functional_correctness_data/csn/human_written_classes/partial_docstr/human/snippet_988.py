from typing import Iterator, Tuple
import re

class Lexer:
    """
    The lexical analysis part.

    This class provides a simple way to define tokens (with patterns)
    to be detected.

    Patterns are provided into a list of 2-uple. Each 2-uple consists
    of a token name and an associated pattern, example:

      [(b"left_bracket", br'\\['),]
    """

    def __init__(self, definitions):
        self.definitions = definitions
        parts = []
        for name, part in definitions:
            param = b'(?P<%s>%s)' % (name, part)
            parts.append(param)
        self.regexpString = b'|'.join(parts)
        self.regexp = re.compile(self.regexpString, re.MULTILINE)
        self.wsregexp = re.compile(b'\\s+', re.M)

    def curlineno(self) -> int:
        """Return the current line number"""
        return self.text[:self.pos].count(b'\n') + 1

    def curcolno(self) -> int:
        """Return the current column number"""
        return self.pos - self.text.rfind(b'\n', 0, self.pos)

    def scan(self, text: bytes) -> Iterator[Tuple[str, bytes]]:
        """Analyse some data

        Analyse the passed content. Each time a token is recognized, a
        2-uple containing its name and parsed value is raised (via
        yield).

        On error, a ParseError exception is raised.

        :param text: a binary string containing the data to parse
        """
        self.pos = 0
        self.text = text
        while self.pos < len(text):
            m = self.wsregexp.match(text, self.pos)
            if m is not None:
                self.pos = m.end()
                continue
            m = self.regexp.match(text, self.pos)
            if m is None:
                token = text[self.pos:]
                m = self.wsregexp.search(token)
                if m is not None:
                    token = token[:m.start()]
                raise ParseError(f'unknown token {token}')
            yield (m.lastgroup, m.group(m.lastgroup))
            self.pos += len(m.group(0))