import re
from typing import TYPE_CHECKING, Any, Callable, Dict, Generic, Iterable, List, NoReturn, Sequence, Set, Sized, Tuple, Type, TypeVar, Union, cast

class Regex:
    """
    Enables schema.py to validate string using regular expressions.
    """
    NAMES = ['re.ASCII', 're.DEBUG', 're.VERBOSE', 're.UNICODE', 're.DOTALL', 're.MULTILINE', 're.LOCALE', 're.IGNORECASE', 're.TEMPLATE']

    def __init__(self, pattern_str: str, flags: int=0, error: Union[str, None]=None) -> None:
        self._pattern_str: str = pattern_str
        flags_list = [Regex.NAMES[i] for i, f in enumerate(f'{flags:09b}') if f != '0']
        self._flags_names: str = ', flags=' + '|'.join(flags_list) if flags_list else ''
        self._pattern: re.Pattern = re.compile(pattern_str, flags=flags)
        self._error: Union[str, None] = error

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self._pattern_str!r}{self._flags_names})'

    @property
    def pattern_str(self) -> str:
        """The pattern string for the represented regular expression"""
        return self._pattern_str

    def validate(self, data: str, **kwargs: Any) -> str:
        """
        Validates data using the defined regex.
        :param data: Data to be validated.
        :return: Returns validated data.
        """
        e = self._error
        try:
            if self._pattern.search(data):
                return data
            else:
                error_message = e.format(data) if e else f'{data!r} does not match {self._pattern_str!r}'
                raise SchemaError(error_message)
        except TypeError:
            error_message = e.format(data) if e else f'{data!r} is not string nor buffer'
            raise SchemaError(error_message)