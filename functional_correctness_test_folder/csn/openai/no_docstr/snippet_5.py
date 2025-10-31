
from __future__ import annotations

from typing import Any, Dict, List, Optional


class ExtensionLoaderMixin:
    """
    A mixin that provides a simple mechanism for loading extensions from a
    context dictionary.  The context can be supplied either via the ``context``
    keyword argument or via arbitrary keyword arguments passed to ``__init__``.
    The extensions are expected to be stored under the key ``"extensions"``
    (or ``"extension"`` for backward compatibility) and must be an iterable
    of strings.
    """

    def __init__(
        self,
        *,
        context: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialise the mixin.

        Parameters
        ----------
        context:
            Optional dictionary containing configuration values.  If omitted,
            an empty dictionary is used.
        **kwargs:
            Additional keyword arguments are merged into the context.  This
            allows callers to provide configuration values directly without
            constructing a dictionary.
        """
        # Start with a copy of the supplied context or an empty dict
        self._context: Dict[str, Any] = dict(context or {})
        # Merge any additional keyword arguments into the context
        self._context.update(kwargs)

    def _read_extensions(self, context: Dict[str, Any]) -> List[str]:
        """
        Extract a list of extensions from the provided context.

        The method looks for the key ``"extensions"`` first.  If it is not
        present, it falls back to ``"extension"`` for backward compatibility.
        The value must be an iterable of strings; otherwise a ``ValueError`` is
        raised.

        Parameters
        ----------
        context:
            Dictionary from which to read the extensions.

        Returns
        -------
        List[str]
            A list of extension names.
        """
        # Prefer the plural key, fall back to the singular key
        raw = context.get("extensions", context.get("extension", []))

        # Ensure we have an iterable of strings
        if isinstance(raw, str):
            # Treat a single string as a single extension
            return [raw]
        try:
            # Try to iterate over the value
            extensions = list(raw)
        except TypeError:
            raise ValueError(
                f"Extensions value must be an iterable of strings, got {type(raw)!r}"
            )

        # Validate that each element is a string
        for ext in extensions:
            if not isinstance(ext, str):
                raise ValueError(
                    f"Each extension must be a string, got {type(ext)!r} in {extensions!r}"
                )

        return extensions
