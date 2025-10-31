from queue import Queue, Empty
from threading import Thread
import time

class _StreamReader:
    """
    Allow streams to be read in real-time, with a timeout.

    Works cross-platform, unlike select.
    """

    def __init__(self, stdout_, stderr_):
        self._queue = Queue()
        self._completed_count = 0
        for stream, id in [(stdout_, 'out'), (stderr_, 'err')]:
            t = Thread(target=self._fill_queue, args=(stream, id), daemon=True)
            t.start()

    def _fill_queue(self, stream, id):
        if hasattr(stream, 'read1'):
            while not stream.closed:
                data = stream.read1()
                if data:
                    self._queue.put((data, id))
                elif not stream.closed:
                    time.sleep(0.1)
        else:
            for line in stream:
                self._queue.put((line, id))
        self._queue.put('completed')

    def read(self, timeout=None):
        """
        returns a tuple (stdin_output, stderr_output)
        where one will be None.
        or None if timed out or completed.

        Will block unbounded if timeout is None
        """
        if self._completed_count >= 2:
            return None
        try:
            while True:
                item = self._queue.get(block=True, timeout=timeout)
                if item == 'completed':
                    self._completed_count += 1
                    if self._completed_count == 2:
                        return None
                else:
                    line, id = item
                    if id == 'out':
                        return (line, None)
                    else:
                        return (None, line)
        except Empty:
            return None