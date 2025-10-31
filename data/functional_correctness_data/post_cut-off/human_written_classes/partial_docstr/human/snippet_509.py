from typing import Any, Literal

class EncoderErrors:
    """Encoder errors"""

    @staticmethod
    def circular_reference() -> str:
        return 'Circular reference detected'

    @staticmethod
    def float_out_of_range(obj: Any) -> str:
        return f'Out of range float values are not allowed: {repr(obj)}'

    @staticmethod
    def invalid_key_type(key: Any) -> str:
        return f'keys must be str, int, float, bool or None, not {key.__class__.__name__}'

    @staticmethod
    def unable_to_encode(obj: Any) -> str:
        return f'Object of type {obj.__class__.__name__} is not JSON serializable'

    @staticmethod
    def invalid_typed_dict(obj: Any) -> str:
        return f'Object of type {obj.__class__.__name__} is not a TypedDict'