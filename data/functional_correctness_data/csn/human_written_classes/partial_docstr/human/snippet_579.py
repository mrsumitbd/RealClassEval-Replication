class FilterWrapper:
    """
    Filter function wrapper. Expected to be called as though it's a filter
    function. Since @flaky adds attributes to a decorated class, Python wants
    to turn a bare function into an unbound method, which is not what we want.
    """

    def __init__(self, rerun_filter):
        self._filter = rerun_filter

    def __call__(self, *args, **kwargs):
        return self._filter(*args, **kwargs)