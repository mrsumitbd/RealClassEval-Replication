class _Image:

    def __init__(self, data):
        self.plat_image = self._PlatImage(data.get('plat_image', {}))

    def __repr__(self):
        return str(self.__dict__)

    class _PlatImage:

        def __init__(self, data):
            self.url = data.get('url', None)
            self.width = data.get('width', None)
            self.height = data.get('height', None)
            self.image_id = data.get('image_id', None)

        def __repr__(self):
            return str(self.__dict__)