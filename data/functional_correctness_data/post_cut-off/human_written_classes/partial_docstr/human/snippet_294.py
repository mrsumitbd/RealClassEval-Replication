import inspect
from tilus.lang.script import Script
from hidet.ir.type import DataType, PointerType
from typing import Any, Mapping, Optional, Sequence, Type

class CallParameters:
    """
    Analyze the parameters in the Script '__call__' function.

    We require that each parameter in the '__call__' function has type annotation. The type annotation be either
    - a pythonic constant, e.g., int, float, str, bool, etc.
    - a type from Hidet IR's type system, e.g., hidet.float16, hidet.int32, etc.

    The return annotation of the '__call__' function should always be None for now.

    We treat the pythonic constant parameters as the JIT constants, that is, different values of these parameters will
    trigger different JIT compilations.
    We treat the hidet integer types (hidet.int32, hidet.int64, etc.) as the parameters that will trigger tuning but
    not JIT compilation.
    """

    def __init__(self, script_cls: Type[Script]):
        self.signature: inspect.Signature = inspect.signature(getattr(script_cls, '__call__'))
        self.param_names: list[str] = []
        self.param_types: list[Type[bool] | Type[int] | Type[float] | Type[str] | DataType | PointerType] = []
        self.const_params: list[int] = []
        self.kernel_params: list[int] = []
        self.tuning_params: list[int] = []
        self.with_default: bool = False
        self.extract_params()

    def extract_params(self):
        for index, param in enumerate(list(self.signature.parameters.values())[1:]):
            if param.kind != inspect.Parameter.POSITIONAL_OR_KEYWORD:
                raise ValueError('The parameter kind should be POSITIONAL_OR_KEYWORD for each __call__ parameter.')
            if param.annotation is inspect.Parameter.empty:
                raise ValueError('The following parameter miss type annotation: ' + param.name)
            if param.default is not inspect.Parameter.empty:
                self.with_default = True
            if isinstance(param.annotation, (DataType, PointerType)) or param.annotation in [bool, int, float, str]:
                self.param_names.append(param.name)
                self.param_types.append(param.annotation)
                annotation = param.annotation
                if annotation in [bool, int, float, str]:
                    self.const_params.append(index)
                else:
                    self.kernel_params.append(index)
                    if isinstance(annotation, DataType) and annotation.is_integer():
                        self.tuning_params.append(index)
            elif isinstance(param.annotation, str):
                raise ValueError("The parameter annotation is a string. It's likely that `from __future__ import annotations` is used. Tilus currently does not support this feature and please remove it and try again.")
            else:
                raise ValueError('The type annotation should be a pythonic constant or a Hidet IR type.')
        if self.signature.return_annotation not in [self.signature.empty, None]:
            raise ValueError('The return annotation of the __call__ function should be None or omitted.')