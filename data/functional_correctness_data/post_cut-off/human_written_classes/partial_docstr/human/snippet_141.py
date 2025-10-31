from queue import Queue

class TextStreamer:
    """
    Imitates a queue for streaming text from one thread to another.

    Not needed once we integrate with the lemonade API.
    """

    def __init__(self):
        self.text_queue = Queue()
        self.stop_signal = None

    def add_text(self, text: str):
        self.text_queue.put(text)

    def done(self):
        self.text_queue.put(self.stop_signal)

    def __iter__(self):
        return self

    def __next__(self):
        value = self.text_queue.get()
        if value == self.stop_signal:
            raise StopIteration()
        else:
            return value