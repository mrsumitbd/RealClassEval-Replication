class NullFunc:
    def __call__(self, *args):
        """Do nothing and return None."""
        return None

    def distance(self, other):
        """
        Trivial distance metric that only cares whether the other object is also
        an instance of NullFunc.  Intentionally does not inherit from HARKobject
        as this might create dependency problems.
        Parameters
        ----------
        other : any
            Any object for comparison to this instance of NullFunc.
        Returns
        -------
        float
            The distance between self and other.  Returns 0 if other is also a
            NullFunc; otherwise returns an arbitrary high number.
        """
        if isinstance(other, NullFunc):
            return 0.0
        return float('inf')
