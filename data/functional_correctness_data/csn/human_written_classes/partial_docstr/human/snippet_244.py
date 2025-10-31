class nullcontext:
    """Context manager that does no additional processing.

    Backport from python 3.7+ for older pythons.
    """

    def __init__(self, enter_result=None):
        self.enter_result = enter_result

    def __enter__(self):
        return self.enter_result

    def __exit__(self, *excinfo):
        pass