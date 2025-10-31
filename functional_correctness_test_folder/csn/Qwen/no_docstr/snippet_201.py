
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
        self.name = name
        self.savename = savename if savename is not None else name
        self.filter_coeff = filter_coeff if filter_coeff is not None else [
            'j0', 'j1', 'sin', 'cos']
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

        base_path = os.path.join(path, f'{self.savename}_base.txt')
        np.savetxt(base_path, self.base)

        for coeff in self.filter_coeff:
            coeff_path = os.path.join(path, f'{self.savename}_{coeff}.txt')
            np.savetxt(coeff_path, getattr(self, coeff))

    def fromfile(self, path='filters'):
        '''Load filter values from ASCII-files.
        Load filter base and filter coefficients from ASCII files in the
        directory `path`; `path` can be a relative or absolute path.
        '''
        base_path = os.path.join(path, f'{self.savename}_base.txt')
        self.base = np.loadtxt(base_path)

        for coeff in self.filter_coeff:
            coeff_path = os.path.join(path, f'{self.savename}_{coeff}.txt')
            setattr(self, coeff, np.loadtxt(coeff_path))
