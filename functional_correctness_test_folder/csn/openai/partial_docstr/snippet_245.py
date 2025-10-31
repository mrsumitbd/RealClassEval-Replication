
class Sampleable:
    '''Element who can provide samples'''

    def __init__(self, sample=None):
        """
        Initialize a Sampleable instance.

        Parameters
        ----------
        sample : Any, optional
            A pre‑defined sample value. If not provided, the instance will
            fall back to the default sample defined by :meth:`get_default_sample`.
        """
        self._sample = sample

    def get_sample(self):
        """
        Return the current sample for the element.

        If a sample was supplied during construction, that value is returned.
        Otherwise, the default sample defined by :meth:`get_default_sample` is
        returned.

        Returns
        -------
        Any
            The sample value.
        """
        if self._sample is not None:
            return self._sample
        return self.get_default_sample()

    def get_default_sample(self):
        """
        Return the default value for the element.

        Subclasses may override this method to provide a more meaningful
        default. The base implementation returns ``None``.

        Returns
        -------
        Any
            The default sample value.
        """
        return None
