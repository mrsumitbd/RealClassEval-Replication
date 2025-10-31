import termios
import os

class StreamWriter:
    """StreamWriter reads from some input (the stdin param) and writes to a fd
    (the stream param).  the stdin may be a Queue, a callable, something with
    the "read" method, a string, or an iterable"""

    def __init__(self, log, stream, stdin, bufsize_type, encoding, tty_in):
        self.stream = stream
        self.stdin = stdin
        self.log = log
        self.encoding = encoding
        self.tty_in = tty_in
        self.stream_bufferer = StreamBufferer(bufsize_type, self.encoding)
        self.get_chunk, log_msg = determine_how_to_read_input(stdin)
        self.log.debug('parsed stdin as a %s', log_msg)

    def fileno(self):
        """defining this allows us to do poll on an instance of this
        class"""
        return self.stream

    def write(self):
        """attempt to get a chunk of data to write to our child process's
        stdin, then write it.  the return value answers the questions "are we
        done writing forever?" """
        try:
            chunk = self.get_chunk()
            if chunk is None:
                raise DoneReadingForever
        except DoneReadingForever:
            self.log.debug('done reading')
            if self.tty_in:
                try:
                    char = termios.tcgetattr(self.stream)[6][termios.VEOF]
                except:
                    char = chr(4).encode()
                os.write(self.stream, char)
                os.write(self.stream, char)
            return True
        except NotYetReadyToRead:
            self.log.debug('received no data')
            return False
        if not isinstance(chunk, bytes):
            chunk = chunk.encode(self.encoding)
        for proc_chunk in self.stream_bufferer.process(chunk):
            self.log.debug('got chunk size %d: %r', len(proc_chunk), proc_chunk[:30])
            self.log.debug('writing chunk to process')
            try:
                os.write(self.stream, proc_chunk)
            except OSError:
                self.log.debug('OSError writing stdin chunk')
                return True

    def close(self):
        self.log.debug('closing, but flushing first')
        chunk = self.stream_bufferer.flush()
        self.log.debug('got chunk size %d to flush: %r', len(chunk), chunk[:30])
        try:
            if chunk:
                os.write(self.stream, chunk)
        except OSError:
            pass
        os.close(self.stream)