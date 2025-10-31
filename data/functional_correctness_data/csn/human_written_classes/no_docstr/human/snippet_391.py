class Messages:

    def __init__(self):
        self._stack = []

    def start_context(self):
        self._stack.append([])

    def stop_context(self):
        return self._stack.pop() if self._stack else list()

    def push(self, message):
        self._stack[-1].append(message) if self._stack else self._stack.append([message])