class BaseMedia:
    """
    Different platforms have different ways of representing medias. The goal
    of this object is to provide a way to know which platform the media came
    from and a way to convert it into a media that can be sent to another
    platform.
    """

    def __eq__(self, other):
        raise NotImplementedError

    def __repr__(self):
        raise NotImplementedError