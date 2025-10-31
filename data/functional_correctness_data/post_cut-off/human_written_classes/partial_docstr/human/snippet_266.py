class AutotuneConfig:
    """
    An object that represents a possible kernel configuration for the auto-tuner to try.

    :ivar kwargs: a dictionary of meta-parameters to pass to the kernel as keyword arguments.
    :type kwargs: dict[Str, Any]
    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __setstate__(self, state):
        self.kwargs = state.get('kwargs', {})

    def all_kwargs(self):
        return self.kwargs

    def __str__(self):
        res = []
        for k, v in self.kwargs.items():
            res.append(f'{k}: {v}')
        return ', '.join(res)

    def __hash__(self):
        return hash(tuple(*self.all_kwargs().items()))

    def __eq__(self, other):
        self_tuple = tuple(*self.all_kwargs().items())
        other_tuple = tuple(*other.all_kwargs().items())
        return self_tuple == other_tuple