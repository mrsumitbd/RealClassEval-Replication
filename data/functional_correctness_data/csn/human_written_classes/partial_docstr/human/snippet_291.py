from wsgidav import util
import queue

class FileLikeQueue:
    """A queue for chunks that behaves like a file-like.

    read() and write() are typically called from different threads.

    This helper class is intended to handle use cases where an incoming PUT
    request should be directly streamed to a remote target:

    def begin_write(self, contentType=None):
        # Create a proxy buffer
        queue = FileLikeQueue(max_size=1)
        # ... and use it as source for the consumer:
        requests.post(..., data=queue)
        # pass it to the PUT handler as target
        return queue
    """

    def __init__(self, max_size=0):
        self.is_closed = False
        self.queue = queue.Queue(max_size)
        self.unread = b''

    def read(self, size=0):
        """Read a chunk of bytes from queue.

        size = 0: Read next chunk (arbitrary length)
             > 0: Read one chunk of `size` bytes (or less if stream was closed)
             < 0: Read all bytes as single chunk (i.e. blocks until stream is closed)

        This method blocks until the requested size become available.
        However, if close() was called, '' is returned immediately.
        """
        res = self.unread
        self.unread = b''
        while res == b'' or size < 0 or (size > 0 and len(res) < size):
            try:
                res += self.queue.get(True, 0.1)
            except queue.Empty:
                if self.is_closed:
                    break
        if size > 0 and len(res) > size:
            self.unread = res[size:]
            res = res[:size]
        assert type(res) is bytes
        return res

    def write(self, chunk):
        """Put a chunk of bytes (or an iterable) to the queue.

        May block if max_size number of chunks is reached.
        """
        assert type(chunk) is bytes
        if self.is_closed:
            raise ValueError('Cannot write to closed object')
        if util.is_basestring(chunk):
            self.queue.put(chunk)
        else:
            for o in chunk:
                self.queue.put(o)

    def close(self):
        self.is_closed = True