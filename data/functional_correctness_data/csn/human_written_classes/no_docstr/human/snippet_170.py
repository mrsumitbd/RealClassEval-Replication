class TermColors:

    def __init__(self) -> None:
        self.FILE = '\x1b[33m'
        self.WWORD = '\x1b[31m'
        self.FWORD = '\x1b[32m'
        self.DISABLE = '\x1b[0m'

    def disable(self) -> None:
        self.FILE = ''
        self.WWORD = ''
        self.FWORD = ''
        self.DISABLE = ''