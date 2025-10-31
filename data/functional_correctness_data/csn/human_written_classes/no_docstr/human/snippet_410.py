class LocalMethod:
    __slots__ = ('f', 'f_der', 'f_der2', 'f_der3', 'f_int', 'f_int_over_T')

    def __hash__(self):
        return hash(tuple((id(getattr(self, o)) for o in self.__slots__)))

    def __init__(self, f, f_der, f_der2, f_der3, f_int, f_int_over_T):
        self.f = f
        self.f_der = f_der
        self.f_der2 = f_der2
        self.f_der3 = f_der3
        self.f_int = f_int
        self.f_int_over_T = f_int_over_T