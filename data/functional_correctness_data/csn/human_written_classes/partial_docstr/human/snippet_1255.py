import inspect
import functools

class Task:
    """
    Defines a task and its parameters and dependencies
    """

    def __init__(self, func: callable, *dependencies, default=False, hidden=False, ignore_return_code=False):
        self.name = func.__name__
        self.func = func
        self.dependencies = dependencies
        self.default = default
        self.hidden = hidden
        self.ignore_return_code = ignore_return_code
        self.description = ((inspect.getdoc(func) or '').splitlines() or [''])[0]
        self.parameters = ParameterGroup.from_callable(func, ignored_parameters={'self', 'context'})
        functools.update_wrapper(self, func)

    def __repr__(self):
        parameters = ', '.join(map(repr, self.parameters.values()))
        return f'{self.name}({parameters})'

    def __call__(self, context, **kwargs):
        parameters = self.parameters.to_dict()
        parameters.update(kwargs)
        return_code = self.func(context, **parameters)
        if not (self.ignore_return_code or return_code in (0, None)):
            raise TaskError(f'{self.name} exited with an error')
        return return_code

    @property
    def title_name(self):
        """
        Returns the name of the task for printing
        """
        return self.name.replace('_', ' ')