import numpy as np

class NullFunc:
    """
    A trivial class that acts as a placeholder "do nothing" function.
    """

    def __call__(self, *args):
        """
        Returns meaningless output no matter what the input(s) is.  If no input,
        returns None.  Otherwise, returns an array of NaNs (or a single NaN) of
        the same size as the first input.
        """
        if len(args) == 0:
            return None
        else:
            arg = args[0]
            if hasattr(arg, 'shape'):
                return np.zeros_like(arg) + np.nan
            else:
                return np.nan

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
        (unnamed) : float
            The distance between self and other.  Returns 0 if other is also a
            NullFunc; otherwise returns an arbitrary high number.
        """
        try:
            if other.__class__ is self.__class__:
                return 0.0
            else:
                return 1000.0
        except:
            return 10000.0