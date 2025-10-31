from config.logger import setup_logging

class FunctionRegistry:

    def __init__(self):
        self.function_registry = {}
        self.logger = setup_logging()

    def register_function(self, name, func_item=None):
        if func_item:
            self.function_registry[name] = func_item
            self.logger.bind(tag=TAG).debug(f"函数 '{name}' 直接注册成功")
            return func_item
        func = all_function_registry.get(name)
        if not func:
            self.logger.bind(tag=TAG).error(f"函数 '{name}' 未找到")
            return None
        self.function_registry[name] = func
        self.logger.bind(tag=TAG).debug(f"函数 '{name}' 注册成功")
        return func

    def unregister_function(self, name):
        if name not in self.function_registry:
            self.logger.bind(tag=TAG).error(f"函数 '{name}' 未找到")
            return False
        self.function_registry.pop(name, None)
        self.logger.bind(tag=TAG).info(f"函数 '{name}' 注销成功")
        return True

    def get_function(self, name):
        return self.function_registry.get(name)

    def get_all_functions(self):
        return self.function_registry

    def get_all_function_desc(self):
        return [func.description for _, func in self.function_registry.items()]