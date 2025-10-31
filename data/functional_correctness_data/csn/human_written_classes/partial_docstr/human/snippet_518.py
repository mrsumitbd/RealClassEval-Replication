class __compute_selector_default:
    """
    Using a function instead of setting default to [] in _slot_defaults, as
    if it were modified in place later, which would happen with check_on_set set to False,
    then the object in _slot_defaults would itself be updated and the next Selector
    instance created wouldn't have [] as the default but a populated list.
    """

    def __call__(self, p):
        return []

    def __repr__(self):
        return repr(self.sig)

    @property
    def sig(self):
        return []