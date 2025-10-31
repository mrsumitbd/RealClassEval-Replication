class Description:
    """
    Used to represent a description.

    Will contain text processing methods.
    """

    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text