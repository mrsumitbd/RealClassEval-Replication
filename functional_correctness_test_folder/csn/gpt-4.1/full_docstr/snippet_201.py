
import os
import numpy as np


class DigitalFilter:
    '''Simple Class for Digital Linear Filters.

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
    '''

    def __init__(self, name, savename=None, filter_coeff=None):
        '''Add filter name.'''
        self.name = name
        self.savename = savename if savename is not None else name
        if filter_coeff is None:
            self.filter_coeff = ['j0', 'j1', 'sin', 'cos']
        else:
            self.filter_coeff = filter_coeff
        # Placeholders for base and coefficients
        self.base = None
        for coeff in self.filter_coeff:
            setattr(self, coeff, None)

    def tofile(self, path='filters'):
        '''Save filter values to ASCII-files.
        Store the filter base and the filter coefficients in separate files
        in the directory `path`; `path` can be a relative or absolute path.
        '''
        if not os.path.exists(path):
            os.makedirs(path)
        # Save base
        base_file = os.path.join(path, f"{self.savename}_base.txt")
        if self.base is not None:
            np.savetxt(base_file, self.base)
        # Save coefficients
        for coeff in self.filter_coeff:
            arr = getattr(self, coeff, None)
            if arr is not None:
                coeff_file = os.path.join(path, f"{self.savename}_{coeff}.txt")
                np.savetxt(coeff_file, arr)

    def fromfile(self, path='filters'):
        '''Load filter values from ASCII-files.
        Load filter base and filter coefficients from ASCII files in the
        directory `path`; `path` can be a relative or absolute path.
        '''
        # Load base
        base_file = os.path.join(path, f"{self.name}_base.txt")
        if os.path.isfile(base_file):
            self.base = np.loadtxt(base_file)
        # Load coefficients
        for coeff in self.filter_coeff:
            coeff_file = os.path.join(path, f"{self.name}_{coeff}.txt")
            if os.path.isfile(coeff_file):
                setattr(self, coeff, np.loadtxt(coeff_file))
