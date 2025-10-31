class NullFunc:
    '''
    A trivial class that acts as a placeholder "do nothing" function.
    '''

    def __call__(self, *args):
        '''
        Returns meaningless output no matter what the input(s) is.  If no input,
        returns None.  Otherwise, returns an array of NaNs (or a single NaN) of
        the same size as the first input.
        '''
        if len(args) == 0:
            return None

        first = args[0]

        # Try numpy if available and the input is a numpy array
        try:
            import numpy as np  # type: ignore
            if isinstance(first, np.ndarray):
                return np.full(first.shape, np.nan, dtype=float)
        except Exception:
            pass

        def _nans_like(obj):
            # Handle basic scalar types
            if obj is None:
                return float('nan')
            if isinstance(obj, (int, float, complex, bool, str)):
                return float('nan')

            # Handle sequences: list and tuple (recursively)
            if isinstance(obj, list):
                return [_nans_like(elem) for elem in obj]
            if isinstance(obj, tuple):
                return tuple(_nans_like(elem) for elem in obj)

            # Fallback for other types: single NaN
            return float('nan')

        return _nans_like(first)

    def distance(self, other):
        '''
        Trivial distance metric that only cares whether the other object is also
        an instance of NullFunc.  Intentionally does not inherit from HARKobject
        as this might create dependency problems.
        Parameters
        ----------
        other : any
            Any object for comparison to this instance of NullFunc.
        Returns
        -------
        (unnamed) : float
            The distance between self and other.  Returns 0 if other is also a
            NullFunc; otherwise returns an arbitrary high number.
        '''
        return 0.0 if isinstance(other, NullFunc) else 1e12
