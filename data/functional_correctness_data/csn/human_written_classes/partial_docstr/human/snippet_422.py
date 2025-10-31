class Satellite:
    """
    Databox class representing a satellite

    :param name: the satellite
    :type name: str
    :param symbol: the short name of the satellite
    :type symbol: str
    """

    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

    def __repr__(self):
        return '<%s.%s - name=%s symbol=%s>' % (__name__, self.__class__.__name__, self.name, self.symbol)