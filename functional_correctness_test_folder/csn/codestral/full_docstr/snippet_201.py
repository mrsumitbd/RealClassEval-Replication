
import os


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
        self.filter_coeff = filter_coeff if filter_coeff is not None else [
            'j0', 'j1', 'sin', 'cos']
        self.base = None
        for coeff in self.filter_coeff:
            setattr(self, coeff, None)

    def tofile(self, path='filters'):
        '''Save filter values to ASCII-files.
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
        '''
        if not os.path.exists(path):
            os.makedirs(path)
        with open(os.path.join(path, f'{self.savename}_base.txt'), 'w') as f:
            f.write('\n'.join(map(str, self.base)))
        for coeff in self.filter_coeff:
            with open(os.path.join(path, f'{self.savename}_{coeff}.txt'), 'w') as f:
                f.write('\n'.join(map(str, getattr(self, coeff))))

    def fromfile(self, path='filters'):
        '''Load filter values from ASCII-files.
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
        '''
        with open(os.path.join(path, f'{self.name}_base.txt'), 'r') as f:
            self.base = [float(line.strip()) for line in f.readlines()]
        for coeff in self.filter_coeff:
            with open(os.path.join(path, f'{self.name}_{coeff}.txt'), 'r') as f:
                setattr(self, coeff, [float(line.strip())
                        for line in f.readlines()])
