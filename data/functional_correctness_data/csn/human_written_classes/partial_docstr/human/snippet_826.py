from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from pip_api._vendor.pyparsing import Forward, Group, Literal as L, ParseException, ParseResults, QuotedString, ZeroOrMore, stringEnd, stringStart

class Marker:

    def __init__(self, marker: str) -> None:
        try:
            self._markers = _coerce_parse_result(MARKER.parseString(marker))
        except ParseException as e:
            raise InvalidMarker(f'Invalid marker: {marker!r}, parse error at {marker[e.loc:e.loc + 8]!r}')

    def __str__(self) -> str:
        return _format_marker(self._markers)

    def __repr__(self) -> str:
        return f"<Marker('{self}')>"

    def evaluate(self, environment: Optional[Dict[str, str]]=None) -> bool:
        """Evaluate a marker.

        Return the boolean from evaluating the given marker against the
        environment. environment is an optional argument to override all or
        part of the determined environment.

        The environment is determined from the current Python process.
        """
        current_environment = default_environment()
        if environment is not None:
            current_environment.update(environment)
        return _evaluate_markers(self._markers, current_environment)