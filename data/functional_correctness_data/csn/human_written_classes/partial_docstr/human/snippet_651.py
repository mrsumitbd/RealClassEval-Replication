class Linearization:
    """A linearization of a curve.

    This class is provided as a stand-in for a curve, so it
    provides a similar interface.

    Args:
        curve (SubdividedCurve): A curve that is linearized.
        error (float): The linearization error. Expected to have been
            computed via :func:`linearization_error`.
    """
    __slots__ = ('curve', 'error', 'start_node', 'end_node')

    def __init__(self, curve, error):
        self.curve = curve
        'SubdividedCurve: The curve that this linearization approximates.'
        self.error = error
        'float: The linearization error for the linearized curve.'
        self.start_node = curve.nodes[:, 0]
        'numpy.ndarray: The 1D start vector of this linearization.'
        self.end_node = curve.nodes[:, -1]
        'numpy.ndarray: The 1D end vector of this linearization.'

    @property
    def __dict__(self):
        """dict: Dictionary of current linearization's property namespace.

        This is just a stand-in property for the usual ``__dict__``. This
        class defines ``__slots__`` so by default would not provide a
        ``__dict__``.

        This also means that the current object can't be modified by the
        returned dictionary.
        """
        return {'curve': self.curve, 'error': self.error, 'start_node': self.start_node, 'end_node': self.end_node}

    def subdivide(self):
        """Do-nothing method to match the :class:`.Curve` interface.

        Returns:
            Tuple[~bezier.hazmat.geometric_intersection.Linearization]: List of
            all subdivided parts, which is just the current object.
        """
        return (self,)

    @classmethod
    def from_shape(cls, shape):
        """Try to linearize a curve (or an already linearized curve).

        Args:
            shape (Union[SubdividedCurve,             ~bezier.hazmat.geometric_intersection.Linearization]): A curve or
                an already linearized curve.

        Returns:
            Union[SubdividedCurve,             ~bezier.hazmat.geometric_intersection.Linearization]: The
            (potentially linearized) curve.
        """
        if shape.__class__ is cls:
            return shape
        else:
            error = linearization_error(shape.nodes)
            if error < _ERROR_VAL:
                linearized = cls(shape, error)
                return linearized
            else:
                return shape