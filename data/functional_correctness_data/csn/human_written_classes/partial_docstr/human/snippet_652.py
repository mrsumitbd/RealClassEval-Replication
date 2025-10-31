from bezier.hazmat import curve_helpers

class SubdividedCurve:
    """A data wrapper for a B |eacute| zier curve

    To be used for intersection algorithm via repeated subdivision,
    where the ``start`` and ``end`` parameters must be tracked.

    Args:
        nodes (numpy.ndarray): The control points of the current
            subdivided curve
        original_nodes (numpy.ndarray): The control points of the original
            curve used to define the current one (before subdivision began).
        start (Optional[float]): The start parameter after subdivision.
        end (Optional[float]): The end parameter after subdivision.
    """
    __slots__ = ('nodes', 'original_nodes', 'start', 'end')

    def __init__(self, nodes, original_nodes, start=0.0, end=1.0):
        self.nodes = nodes
        self.original_nodes = original_nodes
        self.start = start
        self.end = end

    @property
    def __dict__(self):
        """dict: Dictionary of current subdivided curve's property namespace.

        This is just a stand-in property for the usual ``__dict__``. This
        class defines ``__slots__`` so by default would not provide a
        ``__dict__``.

        This also means that the current object can't be modified by the
        returned dictionary.
        """
        return {'nodes': self.nodes, 'original_nodes': self.original_nodes, 'start': self.start, 'end': self.end}

    def subdivide(self):
        """Split the curve into a left and right half.

        See :meth:`.Curve.subdivide` for more information.

        Returns:
            Tuple[SubdividedCurve, SubdividedCurve]: The left and right
            sub-curves.
        """
        left_nodes, right_nodes = curve_helpers.subdivide_nodes(self.nodes)
        midpoint = 0.5 * (self.start + self.end)
        left = SubdividedCurve(left_nodes, self.original_nodes, start=self.start, end=midpoint)
        right = SubdividedCurve(right_nodes, self.original_nodes, start=midpoint, end=self.end)
        return (left, right)