class Parser:
    """Parser interface."""
    stdinInput = True
    multipleInput = False

    def __init__(self):
        pass

    def parse(self):
        raise NotImplementedError