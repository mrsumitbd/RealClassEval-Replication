class _Text:

    def __init__(self, data):
        self.text = data.get('text', None)

    def __repr__(self):
        return str(self.__dict__)