class WidestWeight:

    def __init__(self, weight, inverse=True):
        self._value = 1 / weight if inverse else weight

    def __add__(self, weight):
        weight = weight._value if isinstance(weight, WidestWeight) else weight
        return WidestWeight(max(self._value, weight), inverse=False)

    def __radd__(self, weight):
        return self.__add__(weight)

    def __lt__(self, weight):
        weight = weight._value if isinstance(weight, WidestWeight) else weight
        return self._value < weight

    @staticmethod
    def nx_weight(weight='weight'):
        return lambda u, v, data: WidestWeight(data[weight])