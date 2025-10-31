class _Video:

    def __init__(self, data):
        self.plat_video = self._PlatVideo(data.get('plat_video', {}))

    def __repr__(self):
        return str(self.__dict__)

    class _PlatVideo:

        def __init__(self, data):
            self.url = data.get('url', None)
            self.width = data.get('width', None)
            self.height = data.get('height', None)
            self.video_id = data.get('video_id', None)
            self.cover = data.get('cover', {})

        def __repr__(self):
            return str(self.__dict__)

        class _Cover:

            def __init__(self, data):
                self.url = data.get('url', None)
                self.width = data.get('width', None)
                self.height = data.get('height', None)

            def __repr__(self):
                return str(self.__dict__)