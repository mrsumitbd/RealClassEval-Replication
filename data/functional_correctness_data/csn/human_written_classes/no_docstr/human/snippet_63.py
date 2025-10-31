class Protocol:

    def __init__(self, StreamReader):
        self.reader = StreamReader()
        self.events = []
        self.parser = self.run_parser()
        next(self.parser)

    def run_parser(self):
        while True:
            frame = (yield from self.reader.readexactly(2))
            self.events.append(frame)
            frame = (yield from self.reader.readline())
            self.events.append(frame)

    def data_received(self, data):
        self.reader.feed_data(data)
        next(self.parser)
        events, self.events = (self.events, [])
        return events