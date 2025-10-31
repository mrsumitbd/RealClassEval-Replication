class Unlocker:
    """
    Unlocker instances helps to lock and unlock models easily
    """

    def __init__(self, item):
        self.item = item

    def __enter__(self):
        self.item.unlock()
        return self.item

    def __exit__(self, exc_type, exc_value, traceback):
        self.item.lock()