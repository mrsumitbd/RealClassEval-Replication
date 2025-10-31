class Row:

    def __init__(self, block=None, text=None, separatorline=False, paddingchar=' '):
        self.block = block
        self.text = text
        self.separatorline = separatorline
        self.paddingchar = paddingchar

    def __repr__(self):
        return f"<Row '{self.text}' {self.separatorline} '{self.paddingchar}'>"