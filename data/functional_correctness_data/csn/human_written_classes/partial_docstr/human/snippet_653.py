class Intersection:
    """Representation of a curve-curve intersection.

    Args:
        index_first (int): The index of the first curve within a list of
            curves. Expected to be used to index within the three edges of
            a triangle.
        s (float): The parameter along the first curve where the
            intersection occurs.
        index_second (int): The index of the second curve within a list of
            curves. Expected to be used to index within the three edges of
            a triangle.
        t (float): The parameter along the second curve where the
            intersection occurs.
        interior_curve (Optional[             ~bezier.hazmat.intersection_helpers.IntersectionClassification]):
            The classification of the intersection.
    """
    __slots__ = ('index_first', 's', 'index_second', 't', 'interior_curve')

    def __init__(self, index_first, s, index_second, t, interior_curve=None):
        self.index_first = index_first
        'int: Index of the first curve within a list of edges.'
        self.s = s
        'float: The intersection parameter for the first curve.'
        self.index_second = index_second
        'int: Index of the second curve within a list of edges.'
        self.t = t
        'float: The intersection parameter for the second curve.'
        self.interior_curve = interior_curve
        'IntersectionClassification: Which of the curves is on the interior.\n\n        See :func:`.classify_intersection` for more details.\n        '

    @property
    def __dict__(self):
        """dict: Dictionary of current intersection's property namespace.

        This is just a stand-in property for the usual ``__dict__``. This
        class defines ``__slots__`` so by default would not provide a
        ``__dict__``.

        This also means that the current object can't be modified by the
        returned dictionary.
        """
        return {'index_first': self.index_first, 's': self.s, 'index_second': self.index_second, 't': self.t, 'interior_curve': self.interior_curve}