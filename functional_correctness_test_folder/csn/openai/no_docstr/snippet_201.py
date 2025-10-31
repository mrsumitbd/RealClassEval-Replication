
import os
import numpy as np


class DigitalFilter:
    '''Simple Class for Digital Linear Filters.
    Parameters
    ----------
    name : str
        Name of the DFL.
    savename : str, optional
        Name with which the filter is saved. If None (default) it is set to the
        same value as `name`.
    filter_coeff : list of str, optional
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
        # Base and coefficient arrays will be set later
        self.base = None
        for coeff in self.filter_coeff:
            setattr(self, coeff, None)

    def tofile(self, path='filters'):
        '''Save filter values to ASCII-files.
        Store the filter base and the filter coefficients in separate files
        in the directory `path`; `path` can be a relative or absolute path.
        '''
        # Ensure directory exists
        os.makedirs(path, exist_ok=True)

        # Write base
        if self.base is not None:
            base_file = os.path.join(path, f'{self.savename}_base.txt')
            np.savetxt(base_file, self.base, fmt='%.18e')

        # Write each coefficient
        for coeff in self.filter_coeff:
            arr = getattr(self, coeff, None)
            if arr is not None:
                coeff_file = os.path.join(path, f'{self.savename}_{coeff}.txt')
                np.savetxt(coeff_file, arr, fmt='%.18e')

    def fromfile(self, path='filters'):
        '''Load filter values from ASCII-files.
        Load filter base and filter coefficients from ASCII files in the
        directory `path`; `path` can be a relative or absolute path.
        '''
        # Read base
        base_file = os.path.join(path, f'{self.savename}_base.txt')
        if not os.path.isfile(base_file):
            raise FileNotFoundError(f'Base file not found: {base_file}')
        self.base = np.loadtxt(base_file)

        # Read each coefficient
        for coeff in self.filter_coeff:
            coeff_file = os.path.join(path, f'{self.savename}_{coeff}.txt')
            if not os.path.isfile(coeff_file):
                raise FileNotFoundError(
                    f'Coefficient file not found: {coeff_file}')
            setattr(self, coeff, np.loadtxt(coeff_file))
