class IRI:
    """Class for IRIs, storing IRI as a string."""

    def __init__(self, iri: str) -> None:
        self._iri: str = iri

    def __str__(self) -> str:
        return f'<{self._iri}>'

    def __repr__(self) -> str:
        return f'IRI({self._iri})'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, IRI):
            return self._iri == other._iri
        return False

    def __hash__(self) -> int:
        return hash(self._iri)