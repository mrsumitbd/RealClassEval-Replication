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
        self.filter_coeff = list(filter_coeff)
        self.base = None
        # Initialize coefficient attributes if not already set
        for coeff in self.filter_coeff:
            if not hasattr(self, coeff):
                setattr(self, coeff, None)

    def _ensure_dir(self, path):
        import os
        if not os.path.isdir(path):
            os.makedirs(path, exist_ok=True)

    def _coerce_iterable_of_numbers(self, data, name):
        if data is None:
            raise ValueError(f"{name} is None; set it before saving.")
        try:
            iterable = list(data)
        except TypeError:
            raise TypeError(f"{name} must be an iterable of numbers.")
        out = []
        for i, v in enumerate(iterable):
            try:
                out.append(float(v))
            except Exception as e:
                raise ValueError(f"{name}[{i}]='{v}' is not a number.") from e
        if len(out) == 0:
            raise ValueError(f"{name} is empty.")
        return out

    def _write_vector(self, filepath, vec):
        # Write one value per line with high precision
        with open(filepath, 'w', encoding='utf-8') as f:
            for v in vec:
                f.write(f"{v:.18e}\n")

    def _read_vector(self, filepath):
        vals = []
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                s = line.strip()
                if not s or s.startswith('#'):
                    continue
                vals.append(float(s))
        if not vals:
            raise ValueError(f"File '{filepath}' is empty.")
        return vals

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
        import os
        self._ensure_dir(path)
        base_vec = self._coerce_iterable_of_numbers(self.base, "base")
        base_file = os.path.join(path, f"{self.savename}_base.txt")
        self._write_vector(base_file, base_vec)
        for coeff in self.filter_coeff:
            data = getattr(self, coeff, None)
            if data is None:
                continue
            vec = self._coerce_iterable_of_numbers(data, coeff)
            coeff_file = os.path.join(path, f"{self.savename}_{coeff}.txt")
            self._write_vector(coeff_file, vec)
        return self

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
        import os
        base_file = os.path.join(path, f"{self.savename}_base.txt")
        if not os.path.isfile(base_file):
            raise FileNotFoundError(f"Base file not found: '{base_file}'")
        self.base = self._read_vector(base_file)
        for coeff in self.filter_coeff:
            coeff_file = os.path.join(path, f"{self.savename}_{coeff}.txt")
            if os.path.isfile(coeff_file):
                setattr(self, coeff, self._read_vector(coeff_file))
            else:
                setattr(self, coeff, None)
        return self
