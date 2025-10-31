from green.exceptions import InitializerOrFinalizerError
from sys import modules

class InitializerOrFinalizer:
    """
    I represent a command that will be run as either the initializer or the
    finalizer for a worker process.  The only reason I'm a class instead of a
    function is so that I can be instantiated at the creation time of the Pool
    (with the user's customized command to run), but actually run at the
    appropriate time.
    """

    def __init__(self, dotted_function: str) -> None:
        self.module_part = '.'.join(dotted_function.split('.')[:-1])
        self.function_part = '.'.join(dotted_function.split('.')[-1:])

    def __call__(self, *args) -> None:
        if not self.module_part:
            return
        try:
            __import__(self.module_part)
            loaded_function = getattr(modules[self.module_part], self.function_part, None)
        except Exception as e:
            raise InitializerOrFinalizerError(f"Couldn't load '{self.function_part}' - got: {str(e)}")
        if not loaded_function:
            raise InitializerOrFinalizerError("Loaded module '{}', but couldn't find function '{}'".format(self.module_part, self.function_part))
        try:
            loaded_function()
        except Exception as e:
            raise InitializerOrFinalizerError(f"Error running '{self.function_part}' - got: {str(e)}")