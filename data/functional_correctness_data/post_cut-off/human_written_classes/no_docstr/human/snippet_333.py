from queue import Queue

class QueueHandler:

    def __init__(self, q: Queue) -> None:
        self.queue = q

    def write(self, s: str):
        self.queue.put(s)