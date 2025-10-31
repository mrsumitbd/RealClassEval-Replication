class BlankNode:
    """Class for blank nodes, storing BN's identifier as a string."""

    def __init__(self, identifier: str) -> None:
        self._identifier: str = identifier

    def __str__(self) -> str:
        return f'_:{self._identifier}'

    def __repr__(self) -> str:
        return f'BlankNode(identifier={self._identifier})'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, BlankNode):
            return self._identifier == other._identifier
        return False

    def __hash__(self) -> int:
        return hash(self._identifier)