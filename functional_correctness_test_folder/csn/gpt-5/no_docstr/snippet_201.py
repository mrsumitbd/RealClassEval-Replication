import os
from typing import Iterable

try:
    import numpy as _np  # Optional
except Exception:  # pragma: no cover
    _np = None


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
        self.name = str(name)
        self.savename = str(savename) if savename is not None else self.name
        if filter_coeff is None:
            filter_coeff = ['j0', 'j1', 'sin', 'cos']
        if not isinstance(filter_coeff, (list, tuple)):
            raise TypeError("filter_coeff must be a list or tuple of strings.")
        self.filter_coeff = list(map(str, filter_coeff))
        # Users are expected to set: self.base and any of the coefficients
        # as attributes named according to self.filter_coeff (e.g., self.j0)

    def _ensure_dir(self, path):
        os.makedirs(path, exist_ok=True)

    def _as_1d_sequence(self, arr):
        if _np is not None:
            try:
                a = _np.asarray(arr)
                if a.ndim == 0:
                    return [a.item()]
                return a.ravel().tolist()
            except Exception:
                pass
        # Fallback: try to iterate
        if isinstance(arr, (str, bytes)):
            raise TypeError("Array data must be numeric, not string/bytes.")
        if isinstance(arr, Iterable):
            return list(arr)
        return [arr]

    def _write_array_txt(self, filepath, data):
        seq = self._as_1d_sequence(data)
        with open(filepath, 'w', encoding='utf-8') as f:
            for v in seq:
                f.write(f"{str(v)}\n")

    def _read_array_txt(self, filepath):
        vals = []
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                s = line.strip()
                if not s:
                    continue
                try:
                    v = complex(s)
                except Exception:
                    # Try float as fallback
                    v = float(s)
                vals.append(v)
        if _np is not None:
            arr = _np.asarray(vals)
            if _np.all(_np.isreal(arr)):
                arr = arr.real.astype(float)
            return arr
        # Convert to pure float list if all imag parts are zero
        if all((getattr(v, 'imag', 0.0) == 0) for v in vals):
            return [float(getattr(v, 'real', v)) for v in vals]
        return vals  # complex list

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
        self._ensure_dir(path)

        if not hasattr(self, 'base'):
            raise AttributeError(
                "Attribute 'base' not found on filter. Set 'self.base' before saving.")
        basefile = os.path.join(path, f"{self.savename}_base.txt")
        self._write_array_txt(basefile, getattr(self, 'base'))

        for coeff in self.filter_coeff:
            if hasattr(self, coeff):
                coefffile = os.path.join(path, f"{self.savename}_{coeff}.txt")
                self._write_array_txt(coefffile, getattr(self, coeff))

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
        basefile = os.path.join(path, f"{self.savename}_base.txt")
        if not os.path.isfile(basefile):
            raise FileNotFoundError(f"Base file not found: {basefile}")
        self.base = self._read_array_txt(basefile)

        for coeff in self.filter_coeff:
            coefffile = os.path.join(path, f"{self.savename}_{coeff}.txt")
            if os.path.isfile(coefffile):
                setattr(self, coeff, self._read_array_txt(coefffile))
