import numpy
from itertools import product

class SlidingWindowIterator:
    """
    Moves a sliding window over the array, where the first patch is places centered on
    the top-left voxel and outside-of-image values filled with `cval`. The returned
    patches are views if the array.

    All yielded patches will be of size ``psize``. Areas outside of the array are
    filled with ``cval``. Besides the patch, a patch mask is returned, that denoted
    the outside values.

    Central element for even patches:

        [[0, 0],
         [0, X]]

    Parameters
    ----------
    array : array_like
        A n-dimensional array.
    psize : int or sequence of ints
        The patch size. If a single integer interpreted as hyper-cube.
    cval : number
        Value to fill undefined positions.
    """

    def __init__(self, array, psize, cval=0):
        self.array = numpy.asarray(array)
        if is_integer(psize):
            self.psize = [psize] * self.array.ndim
        else:
            self.psize = list(psize)
        self.cval = cval
        if numpy.any([x <= 0 for x in self.psize]):
            raise ValueError('The patch size must be at least 1 in any dimension.')
        elif len(self.psize) != self.array.ndim:
            raise ValueError('The patch dimensionality must equal the array dimensionality.')
        self.padding = [(p / 2, p / 2 - (p - 1) % 2) for p in self.psize]
        self.array = numpy.pad(self.array, self.padding, mode='constant', constant_values=self.cval)
        slicepoints = [list(range(0, s - p + 1)) for s, p in zip(self.array.shape, self.psize)]
        self.__slicepointiter = product(*slicepoints)

    def __iter__(self):
        return self

    def __next__(self):
        """
        Yields the next patch.

        Returns
        -------
        patch : ndarray
            The extracted patch as a view.
        pmask : ndarray
            Boolean array denoting the defined part of the patch.
        slicer : tuple
            Tuple of slicers to apply the same operation to another array (using applyslicer()).
        """
        spointset = next(self.__slicepointiter)
        slicer = []
        padder = []
        for dim, sp in enumerate(spointset):
            slicer.append(slice(sp, sp + self.psize[dim]))
            padder.append((max(0, -1 * (sp - self.padding[dim][0])), max(0, sp + self.psize[dim] - (self.array.shape[dim] - 1))))
        def_slicer = [slice(x, None if 0 == y else -1 * y) for x, y in padder]
        patch = self.array[tuple(slicer)]
        patch = patch.reshape(self.psize)
        pmask = numpy.zeros(self.psize, numpy.bool_)
        pmask[tuple(def_slicer)] = True
        return (patch, pmask, tuple(slicer))
    next = __next__

    def applyslicer(self, array, slicer, cval=None):
        """
        Apply a slicer returned by the iterator to a new array of the same
        dimensionality as the one used to initialize the iterator.

        Notes
        -----
        If ``array`` has more dimensions than ``slicer`` and ``pmask``, the first ones
        are sliced.

        Parameters
        ----------
        array : array_like
            A n-dimensional array.
        slicer : tuple
            Tuple if `slice()` instances as returned by `next()`.
        cval : number
            Value to fill undefined positions. If None, the ``cval`` of the object is used.

        Returns
        -------
        patch: ndarray
            A patch from the input ``array``.
        """
        if cval is None:
            cval = self.cval
        _padding = self.padding + [(0, 0)] * (array.ndim - len(self.padding))
        array = numpy.pad(array, _padding, mode='constant', constant_values=cval)
        _psize = self.psize + list(array.shape[len(self.psize):])
        return array[tuple(slicer)].reshape(_psize)