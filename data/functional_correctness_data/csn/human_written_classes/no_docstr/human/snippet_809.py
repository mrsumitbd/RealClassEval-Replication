class StreamTransport:

    def __init__(self, stream):
        if isinstance(stream, text_stream_types):
            self.text_mode = True
        elif isinstance(stream, bytes_stream_types):
            self.text_mode = False
        else:
            raise ValueError('Stream is not of a valid stream type')
        if not stream.writable():
            raise ValueError('Stream is not a writeable stream')
        self.stream = stream

    def transmit(self, syslog_msg):
        syslog_msg = syslog_msg + b'\n'
        if self.text_mode:
            syslog_msg = syslog_msg.decode(self.stream.encoding, 'replace')
        self.stream.write(syslog_msg)

    def close(self):
        pass