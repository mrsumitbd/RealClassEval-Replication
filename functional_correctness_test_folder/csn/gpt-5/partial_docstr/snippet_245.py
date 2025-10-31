class Sampleable:
    '''Element who can provide samples
    '''

    def __init__(self, sampler=None, default=None, rng=None):
        import random
        self._default = default
        self._rng = rng if rng is not None else random.Random()
        # Normalize sampler:
        # - callable: use directly
        # - sequence: sample via choice
        # - iterable (non-sequence): materialize to tuple
        self._sampler = None
        if sampler is None:
            self._sampler = None
        elif callable(sampler):
            self._sampler = sampler
        else:
            # Try to recognize a sequence (has __len__ and __getitem__)
            is_sequence = hasattr(sampler, "__len__") and hasattr(
                sampler, "__getitem__")
            if is_sequence:
                self._sampler = sampler
            else:
                # Fallback: try to materialize iterable to a tuple
                try:
                    self._sampler = tuple(sampler)
                except TypeError:
                    # Not iterable; treat as a constant default
                    self._sampler = None
                    self._default = sampler

    def get_sample(self):
        '''Return the a sample for the element
        '''
        if self._sampler is None:
            return self._default
        # Callable sampler
        if callable(self._sampler):
            sampler = self._sampler
            try:
                return sampler()
            except TypeError:
                try:
                    return sampler(self._rng)
                except TypeError:
                    # Last resort: ignore signature issues
                    return self._default
        # Sequence-like sampler
        try:
            if len(self._sampler) == 0:
                return self.get_default_sample()
            idx = self._rng.randrange(len(self._sampler))
            return self._sampler[idx]
        except Exception:
            # Fallback in case sampler isn't indexable as expected
            return self.get_default_sample()

    def get_default_sample(self):
        '''Return default value for the element
        '''
        return self._default
