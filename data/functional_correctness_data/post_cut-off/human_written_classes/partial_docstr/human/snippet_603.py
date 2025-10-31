class Literal:
    """
    Class for literals.

    Notes:
        Consists of: lexical form, and optional language tag and datatype.
        All parts of literal are stored as strings.

    """

    def __init__(self, lex: str, langtag: str | None=None, datatype: str | None=None) -> None:
        self._lex: str = lex
        self._langtag: str | None = langtag
        self._datatype: str | None = datatype

    def __str__(self) -> str:
        suffix = ''
        if self._langtag:
            suffix = f'@{self._langtag}'
        elif self._datatype:
            suffix = f'^^<{self._datatype}>'
        return f'"{self._lex}"{suffix}'

    def __repr__(self) -> str:
        return f'Literal({self._lex!r}, langtag={self._langtag!r}, datatype={self._datatype!r})'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Literal):
            return self._lex == other._lex and self._langtag == other._langtag and (self._datatype == other._datatype)
        return False

    def __hash__(self) -> int:
        return hash((self._lex, self._langtag, self._datatype))