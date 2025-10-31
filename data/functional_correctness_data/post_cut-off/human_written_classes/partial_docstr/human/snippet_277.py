from threading import Thread, Lock

class BroadcastQueue:
    """A simple broadcast queue that duplicates items to all subscribers."""

    def __init__(self):
        self.subscribers = []
        self.lock = Lock()

    def subscribe(self):
        q = FIFOQueue()
        with self.lock:
            self.subscribers.append(q)
        return q

    def push(self, item):
        with self.lock:
            for q in self.subscribers:
                q.push(item)

    def clear(self):
        with self.lock:
            for q in self.subscribers:
                q.clear()