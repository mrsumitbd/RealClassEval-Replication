from typing import Any, Callable, Dict, Iterator, List, Literal, Optional, Tuple, Union, get_args, get_origin
from argparse import OPTIONAL, ZERO_OR_MORE, ArgumentParser

class TypingHintArgSpecGuesser:
    BASIC_TYPES = (str, int, float, bool)

    @classmethod
    def typing_hint_to_arg_spec_params(cls, type_def: type, is_positional: bool=False) -> Dict[str, Any]:
        origin = get_origin(type_def)
        args = get_args(type_def)
        if type_def in cls.BASIC_TYPES:
            return {'type': type_def}
        if type_def in (list, List):
            return {'nargs': ZERO_OR_MORE}
        if origin == Literal:
            return {'choices': args, 'type': type(args[0])}
        if any((origin is t for t in UNION_TYPES)):
            retval = {}
            first_subtype = args[0]
            if first_subtype in cls.BASIC_TYPES:
                retval['type'] = first_subtype
            if first_subtype in (list, List):
                retval['nargs'] = ZERO_OR_MORE
            if first_subtype != List and get_origin(first_subtype) == list:
                retval['nargs'] = ZERO_OR_MORE
                item_type = cls._extract_item_type_from_list_type(first_subtype)
                if item_type:
                    retval['type'] = item_type
            if type(None) in args:
                retval['required'] = False
            return retval
        if origin == list:
            retval = {}
            retval['nargs'] = ZERO_OR_MORE
            if args[0] in cls.BASIC_TYPES:
                retval['type'] = args[0]
            return retval
        return {}

    @classmethod
    def _extract_item_type_from_list_type(cls, type_def) -> Optional[type]:
        args = get_args(type_def)
        if args[0] in cls.BASIC_TYPES:
            return args[0]
        return None