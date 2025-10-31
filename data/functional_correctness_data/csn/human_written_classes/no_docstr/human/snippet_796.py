import json
import threading

class Stream:

    def __init__(self, url, stream_handler):
        self.url = url
        self.stream_handler = stream_handler
        self.sse = None
        self.thread = None
        self.start()

    def start(self):
        self.thread = threading.Thread(target=self.start_stream, args=(self.url, self.stream_handler))
        self.thread.start()
        return self

    def start_stream(self, url, stream_handler):
        self.sse = ClosableSSEClient(url)
        for msg in self.sse:
            msg_data = json.loads(msg.data)
            if msg_data:
                msg_data['event'] = msg.event
                stream_handler(msg_data)

    def close(self):
        self.sse.close()
        self.thread.join()
        return self