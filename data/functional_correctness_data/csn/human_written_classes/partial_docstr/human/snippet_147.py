class SequentialPool:
    """API of a Joblib Parallel pool but sequential execution"""

    def __init__(self):
        self.n_jobs = 1

    def __call__(self, jobs):
        return [fun(*args, **kwargs) for fun, args, kwargs in jobs]