class Creating:
    """
    Creating instances helps to mark and unmark models as creating easily
    """

    def __init__(self, item):
        self.item = item

    def __enter__(self):
        self.item.start_creation()
        return self.item

    def __exit__(self, exc_type, exc_value, traceback):
        self.item.end_creation()