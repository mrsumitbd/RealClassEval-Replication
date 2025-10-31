from sen.util import log_traceback, OrderedSet
from concurrent.futures.thread import ThreadPoolExecutor

class ConcurrencyMixin:

    def __init__(self):
        self.worker = ThreadPoolExecutor(max_workers=4)
        self.ui_worker = ThreadPoolExecutor(max_workers=2)

    @staticmethod
    def _run(worker, f, *args, **kwargs):
        f = log_traceback(f)
        worker.submit(f, *args, **kwargs)

    def run_in_background(self, task, *args, **kwargs):
        logger.info('running task %r(%s, %s) in background', task, args, kwargs)
        self._run(self.worker, task, *args, **kwargs)

    def run_quickly_in_background(self, task, *args, **kwargs):
        logger.info('running a quick task %r(%s, %s) in background', task, args, kwargs)
        self._run(self.ui_worker, task, *args, **kwargs)