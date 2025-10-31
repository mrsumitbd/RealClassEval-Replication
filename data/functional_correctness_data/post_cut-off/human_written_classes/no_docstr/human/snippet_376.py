from typing import Dict, Type, Union

class DataParserFactory:
    _loaders: Dict[str, Type] = {}

    @classmethod
    def register_loader(cls, format_name: str):

        def decorator(loader_class: Type):
            cls._loaders[format_name.lower()] = loader_class
            return loader_class
        return decorator

    @classmethod
    def get_loader(cls, format_name: str, **kwargs) -> object:
        loader_class = cls._loaders.get(format_name.lower())
        if not loader_class:
            available = ', '.join(cls._loaders.keys())
            raise ValueError(f'No loader for {format_name} now. Available: {available}')
        return loader_class(**kwargs) if loader_class else None