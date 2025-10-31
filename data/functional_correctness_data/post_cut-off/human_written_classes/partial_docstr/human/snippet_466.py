class WaitJobsWrapper:
    """
    Wrapper class to wait all jobs
    """

    def __init__(self, pool: 'WorkerPool'):
        self.pool: 'WorkerPool' = pool
        self.jobs: 'list[Job[ResultT]]' = []

    def get(self):
        for job in self.jobs:
            job.get()
        self.jobs.clear()

    def __enter__(self):
        self.jobs.clear()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.get()

    def start_thread_soon(self, func, *args, **kwargs):
        """
        Run a function on thread,
        result can be got from `job` object

        Args:
            func (Callable[..., ResultT]):
            *args:
            **kwargs:

        Returns:
            Job[ResultT]:
        """
        job = self.pool.start_thread_soon(func, *args, **kwargs)
        self.jobs.append(job)
        return job