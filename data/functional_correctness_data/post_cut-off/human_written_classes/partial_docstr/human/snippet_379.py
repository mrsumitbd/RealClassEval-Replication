import importlib

class LazyCallable:
    """延迟可调用对象，在首次调用时导入并执行实际函数"""

    def __init__(self, module_name: str, func_name: str):
        self.module_name = module_name
        self.func_name = func_name
        self._real_func = None

    def __call__(self, *args, **kwargs):
        if self._real_func is None:
            module = importlib.import_module(self.module_name)
            _LOADED_LAZY_MODULES.add(self.module_name)
            self._real_func = getattr(module, self.func_name)
        return self._real_func(*args, **kwargs)