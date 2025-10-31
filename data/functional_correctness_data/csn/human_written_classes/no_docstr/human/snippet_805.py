class _PrettyOutputToStr:

    def __init__(self):
        self.result = ''

    def save_output(self, text=None, nl=True):
        text = text or ''
        self.result += text
        if nl:
            self.result += '\n'