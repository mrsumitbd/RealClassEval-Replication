class PresetEnum:
    """
    Allowed presets for satellite images on Agro API 1.0

    """
    TRUE_COLOR = 'truecolor'
    FALSE_COLOR = 'falsecolor'
    NDVI = 'ndvi'
    EVI = 'evi'

    @classmethod
    def items(cls):
        """
        All values for this enum
        :return: list of str

        """
        return [cls.TRUE_COLOR, cls.FALSE_COLOR, cls.NDVI, cls.EVI]

    def __repr__(self):
        return '<%s.%s>' % (__name__, self.__class__.__name__)