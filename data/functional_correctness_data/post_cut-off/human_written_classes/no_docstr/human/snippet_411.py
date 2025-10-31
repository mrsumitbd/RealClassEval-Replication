class _Url:

    def __init__(self, data):
        self.url = data.get('url', None)
        self.desc = data.get('desc', None)

    def __repr__(self):
        return str(self.__dict__)