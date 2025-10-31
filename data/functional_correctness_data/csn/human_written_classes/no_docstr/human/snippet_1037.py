class Task:

    def __init__(self, func, context_name=None, pre_condition=True, body_params=()):
        self.func = func
        self.name = func.__name__.encode('utf8')
        self.context_name = context_name
        self.pre_condition = pre_condition
        self.body_params = set(body_params)
        self.__name__ = func.__name__
        self.__module__ = func.__module__
        self.__doc__ = func.__doc__

    def __call__(self, *args, **kwargs):
        if self.pre_condition and spooler.installed:
            spooler.schedule(self, args, kwargs)
            return
        try:
            if self.context_name:
                kwargs[self.context_name] = Context(spooled=False)
            self.func(*args, **kwargs)
        except:
            logger.exception('Spooler task %s failed with uncaught exception', self.name)
            raise