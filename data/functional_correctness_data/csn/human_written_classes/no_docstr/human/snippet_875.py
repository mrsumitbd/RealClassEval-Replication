from typing import Callable, Dict, List, Optional, Union

class _ObjectType:
    name: Optional[str] = None
    egg_protocols: Optional[List[Union[str, List[str]]]] = None
    config_prefixes: Optional[List[Union[List[str], str]]] = None

    def __init__(self):
        self.egg_protocols = [_aslist(p) for p in _aslist(self.egg_protocols)]
        self.config_prefixes = [_aslist(p) for p in _aslist(self.config_prefixes)]

    def __repr__(self):
        return '<{} protocols={!r} prefixes={!r}>'.format(self.name, self.egg_protocols, self.config_prefixes)

    def invoke(self, context):
        assert context.protocol in _flatten(self.egg_protocols)
        return fix_call(context.object, context.global_conf, **context.local_conf)