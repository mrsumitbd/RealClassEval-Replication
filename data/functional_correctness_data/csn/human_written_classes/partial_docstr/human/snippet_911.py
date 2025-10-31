from typing import Any, Optional, Union, cast

class Name:
    """Class to describe Avro name."""

    def __init__(self, name_attr: Optional[str]=None, space_attr: Optional[str]=None, default_space: Optional[str]=None) -> None:
        """
        Formulate full name according to the specification.

        @arg name_attr: name value read in schema or None.
        @arg space_attr: namespace value read in schema or None.
        @ard default_space: the current default space or None.
        """

        def validate(val: Optional[str], name: str) -> None:
            if isinstance(val, str) and val != '' or val is None:
                return
            fail_msg = f'{name} must be non-empty string or None.'
            raise SchemaParseException(fail_msg)
        validate(name_attr, 'Name')
        validate(space_attr, 'Space')
        validate(default_space, 'Default space')
        self._full: Optional[str] = name_attr
        if name_attr is None or name_attr == '':
            return
        if name_attr.find('.') < 0:
            if space_attr is not None and space_attr != '':
                self._full = f'{space_attr}.{name_attr}'
            elif default_space is not None and default_space != '':
                self._full = f'{default_space}.{name_attr}'

    @property
    def fullname(self) -> Optional[str]:
        return self._full

    def get_space(self) -> Optional[str]:
        """Back out a namespace from full name."""
        if self._full is None:
            return None
        if self._full.find('.') > 0:
            return self._full.rsplit('.', 1)[0]
        return None