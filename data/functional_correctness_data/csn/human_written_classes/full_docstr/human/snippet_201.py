import numpy as np
import os

class DigitalFilter:
    """Simple Class for Digital Linear Filters.


    Parameters
    ----------
    name : str
        Name of the DFL.

    savename = str
        Name with which the filter is saved. If None (default) it is set to the
        same value as `name`.

    filter_coeff = list of str
        By default, the following filter coefficients are checked:

            ``filter_coeff = ['j0', 'j1', 'sin', 'cos']``

        This accounts for the standard Hankel and Fourier DLF in CSEM
        modelling. However, additional coefficient names can be provided via
        this parameter (in list format).

    """

    def __init__(self, name, savename=None, filter_coeff=None):
        """Add filter name."""
        self.name = name
        if savename is None:
            self.savename = name
        else:
            self.savename = savename
        self.filter_coeff = ['j0', 'j1', 'sin', 'cos']
        if filter_coeff is not None:
            self.filter_coeff.extend(filter_coeff)

    def tofile(self, path='filters'):
        """Save filter values to ASCII-files.

        Store the filter base and the filter coefficients in separate files
        in the directory `path`; `path` can be a relative or absolute path.

        Examples
        --------
        >>> import empymod
        >>> # Load a filter
        >>> filt = empymod.filters.Hankel().wer_201_2018
        >>> # Save it to pure ASCII-files
        >>> filt.tofile()
        >>> # This will save the following three files:
        >>> #    ./filters/wer_201_2018_base.txt
        >>> #    ./filters/wer_201_2018_j0.txt
        >>> #    ./filters/wer_201_2018_j1.txt

        """
        name = self.savename
        path = os.path.abspath(path)
        os.makedirs(path, exist_ok=True)
        basefile = os.path.join(path, name + '_base.txt')
        with open(basefile, 'w') as f:
            self.base.tofile(f, sep='\n')
        for val in self.filter_coeff:
            if hasattr(self, val):
                attrfile = os.path.join(path, name + '_' + val + '.txt')
                with open(attrfile, 'w') as f:
                    getattr(self, val).tofile(f, sep='\n')

    def fromfile(self, path='filters'):
        """Load filter values from ASCII-files.

        Load filter base and filter coefficients from ASCII files in the
        directory `path`; `path` can be a relative or absolute path.

        Examples
        --------
        >>> import empymod
        >>> # Create an empty filter;
        >>> # Name has to be the base of the text files
        >>> filt = empymod.filters.DigitalFilter('my-filter')
        >>> # Load the ASCII-files
        >>> filt.fromfile()
        >>> # This will load the following three files:
        >>> #    ./filters/my-filter_base.txt
        >>> #    ./filters/my-filter_j0.txt
        >>> #    ./filters/my-filter_j1.txt
        >>> # and store them in filt.base, filt.j0, and filt.j1.

        """
        name = self.savename
        path = os.path.abspath(path)
        basefile = os.path.join(path, name + '_base.txt')
        with open(basefile, 'r') as f:
            self.base = np.fromfile(f, sep='\n')
        for val in self.filter_coeff:
            attrfile = os.path.join(path, name + '_' + val + '.txt')
            if os.path.isfile(attrfile):
                with open(attrfile, 'r') as f:
                    setattr(self, val, np.fromfile(f, sep='\n'))
        self.factor = np.around([self.base[1] / self.base[0]], 15)