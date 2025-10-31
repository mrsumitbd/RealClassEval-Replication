class Comment:

    def __init__(self, text):
        self.text = text

    def write(self, f):
        f.write(f'<!--{self.text}-->\n')