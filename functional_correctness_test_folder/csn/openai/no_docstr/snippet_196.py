class Mechanism:
    def __init__(self, mechanism, param=None):
        """
        Initialize a Mechanism instance.

        Parameters
        ----------
        mechanism : Any
            The core mechanism object or identifier.
        param : Any, optional
            Optional parameter(s) associated with the mechanism.
        """
        self.mechanism = mechanism
        self.param = param

    def to_native(self):
        """
        Convert the Mechanism instance into a native representation.

        Returns
        -------
        Any
            If `param` is None, returns the mechanism itself.
            Otherwise, returns a tuple of (mechanism, param).
        """
        if self.param is None:
            return self.mechanism
        return (self.mechanism, self.param)
