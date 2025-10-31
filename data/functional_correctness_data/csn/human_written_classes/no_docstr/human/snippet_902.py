from collections import OrderedDict
import typing

class CaseInsensitive:

    def __init__(self, **kwargs: typing.Dict[str, typing.Union[str, typing.Dict[str, typing.Any], typing.List[typing.Any]]]) -> None:
        keys: typing.List[str] = list(kwargs.keys())
        for k in keys:
            if not k.startswith('_'):
                assert k in kwargs
                setattr(self, k, kwargs[k])

    def __getattr__(self, item: str) -> typing.Union[str, typing.Dict[str, typing.Any], typing.List]:
        keys: typing.List[str] = list(self.__class__.__dict__.keys())
        for k in keys:
            if k.lower() == item.lower():
                value: typing.Optional[typing.Union[str, typing.Dict[str, typing.Any], typing.List]] = self.__dict__.get(k)
                assert value is not None and isinstance(value, (str, dict, list))
                return value
        raise AttributeError(item)

    def __setattr__(self, item: str, value: typing.Union[str, typing.Dict[str, typing.Any], typing.List]) -> None:
        assert isinstance(value, (str, dict)), ValueError(f'got type {str(type(value))}, expected str')
        keys: typing.List[str] = list(self.__class__.__dict__.keys())
        for k in keys:
            if k.lower() == item.lower():
                self.__dict__[k] = value
                return
        if not item.startswith('_'):
            self.__dict__[item] = value
            return
        raise AttributeError(item)

    def as_dict(self) -> typing.Dict[str, typing.Union[str, typing.Dict[str, typing.Any], typing.List]]:
        result: typing.Dict[str, typing.Union[str, typing.Dict[str, typing.Any], typing.List]] = OrderedDict()
        keys: typing.List[str] = list(self.__dict__.keys())
        for k in keys:
            if not k.startswith('_'):
                result[k] = self.__getattr__(k)
        return result