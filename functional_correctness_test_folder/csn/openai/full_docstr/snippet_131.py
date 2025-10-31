
import numpy as np


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
        if not args:
            return None

        first = args[0]
        try:
            # Try to interpret as array-like
            arr = np.asarray(first)
            if arr.ndim == 0:
                # Scalar input
                return np.nan
            else:
                return np.full_like(arr, np.nan, dtype=float)
        except Exception:
            # Fallback: return a single NaN
            return np.nan

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
        return 0.0 if isinstance(other, NullFunc) else 1e6
