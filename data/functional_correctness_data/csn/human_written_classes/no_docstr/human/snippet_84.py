import time

class EventBuffer:

    def __init__(self):
        self.buffer = {}

    def push(self, type, count=1):
        timestamp = int(time.time()) * 1000
        key = f'{timestamp};{type}'
        if key not in self.buffer:
            self.buffer[key] = {'timestamp': timestamp, 'type': type, 'count': count}
        else:
            self.buffer[key]['count'] += count

    def get_and_clear(self):
        buffer = self.buffer
        self.buffer = {}
        return [value for value in buffer.values()]