class Callback:
    """
    a base class for callbacks
    """

    def on_error(self, exception, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        try:
            result = self.run(*args, **kwargs)
        except Exception as e:
            self.on_error(e, *args, kwargs)
            raise e
        return result

    def run(self, *args, **kwargs):
        raise NotImplementedError(f'run is not implemented for {type(self).__name__}!')