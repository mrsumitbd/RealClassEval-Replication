from typing import Type, Optional

class BaseOptions:
    name: Optional[str] = None
    description: Optional[str] = None
    _frozen: bool = False

    def __init__(self, class_type: Type):
        self.class_type: Type = class_type

    def freeze(self):
        self._frozen = True

    def __setattr__(self, name, value):
        if not self._frozen:
            super(BaseOptions, self).__setattr__(name, value)
        else:
            raise Exception(f"Can't modify frozen Options {self}")

    def __repr__(self):
        return f'<{self.__class__.__name__} name={repr(self.name)}>'