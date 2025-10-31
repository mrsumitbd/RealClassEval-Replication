class __compute_length_of_default:

    def __call__(self, p):
        return len(p.default)

    def __repr__(self):
        return repr(self.sig)

    @property
    def sig(self):
        return None