class __compute_selector_checking_default:

    def __call__(self, p):
        return len(p.objects) != 0

    def __repr__(self):
        return repr(self.sig)

    @property
    def sig(self):
        return None