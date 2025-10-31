import threading
from six.moves import queue
import six

class VectorThread:

    def __init__(self, targets):
        self.targets = targets
        self.results = None

    def start_all(self):
        self.thread_handles = []
        for target in self.targets:
            q = queue.Queue()
            t = threading.Thread(target=_ret_via_queue, args=(target, q))
            self.thread_handles.append((t, q))
            t.start()

    def join_all(self, raise_exceptions=True):
        if self.results:
            return self.results
        for t, q in self.thread_handles:
            t.join()
        self.results = [q.get() for _, q in self.thread_handles]
        if raise_exceptions:
            for result in self.results:
                if 'exception' in result:
                    exc_info = result['exception']
                    six.reraise(*exc_info)
        return [x.get('return', None) for x in self.results]