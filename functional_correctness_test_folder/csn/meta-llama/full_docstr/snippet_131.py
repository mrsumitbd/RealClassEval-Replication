
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
        elif isinstance(args[0], np.ndarray):
            return np.full_like(args[0], np.nan)
        else:
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
        if isinstance(other, NullFunc):
            return 0.0
        else:
            return 1e30
