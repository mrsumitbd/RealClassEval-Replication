from typing import Dict, Type, Callable

class Registry:

    def __init__(self):
        self._builders: Dict[Type['TaskBase'], Type['TaskBuilderBase']] = {}
        self._config_factories: Dict[Type['TaskBase'], Callable] = {}
        self._codegens: Dict[Type['TaskBase'], Callable] = {}
        self._op_mapping: Dict[str, Type['TaskBase']] = {}

    def register_task(self, op_type: str, task_cls: Type['TaskBase'], config_factory: Callable, codegen_func: Callable):

        def decorator(builder_cls: Type['TaskBuilderBase']):
            self._builders[task_cls] = builder_cls
            self._config_factories[task_cls] = config_factory
            self._codegens[task_cls] = codegen_func
            self._op_mapping[op_type] = task_cls
            builder_cls._create_config = config_factory
            return builder_cls
        return decorator

    def get_op_mapping(self, op_type: str) -> Type['TaskBase']:
        if op_type not in self._op_mapping:
            raise ValueError(f'Unsupport Op {op_type}')
        return self._op_mapping[op_type]

    def get_builder(self, task_cls: Type['TaskBase']) -> Type['TaskBuilderBase']:
        if task_cls not in self._builders:
            raise ValueError(f'No builder registered for task class {task_cls.__name__}')
        return self._builders[task_cls]

    def get_config_factory(self, task_cls: Type['TaskBase']) -> Callable:
        if task_cls not in self._config_factories:
            raise ValueError(f'No config factor registered for task class {task_cls.__name__}')
        return self._config_factories[task_cls]

    def get_codegen(self, task_cls: Type['TaskBase']) -> Callable:
        if task_cls not in self._codegens:
            raise ValueError(f'No codegen registered for task class {task_cls.__name__}')
        return self._codegens[task_cls]