class PaletteEnum:
    """
    Allowed color palettes for satellite images on Agro API 1.0

    """
    GREEN = '1'
    BLACK_AND_WHITE = '2'
    CONTRAST_SHIFTED = '3'
    CONTRAST_CONTINUOUS = '4'

    @classmethod
    def items(cls):
        """
        All values for this enum
        :return: list of str

        """
        return [cls.GREEN, cls.BLACK_AND_WHITE, cls.CONTRAST_SHIFTED, cls.CONTRAST_CONTINUOUS]

    def __repr__(self):
        return '<%s.%s>' % (__name__, self.__class__.__name__)