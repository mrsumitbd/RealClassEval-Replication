import libdlf
import numpy as np

class _BaseFilter:
    """Base class for wrappers loading filters from libdlf."""

    def __init__(self, ftype):
        """Initiate a new wrapper of `ftype` ('hankel' or 'fourier')."""
        self._ftype = ftype
        self.available = list(FILTERS[ftype].keys())
        for k, v in FILTERS[ftype].items():
            setattr(self, k, v)

    def __getattribute__(self, name):
        """Modify to load filter if the attribute is a know filter name."""
        ftype = object.__getattribute__(self, '_ftype')
        if name in FILTERS[ftype].keys():
            if FILTERS[ftype][name] is None:
                data = getattr(getattr(libdlf, ftype), name)
                dlf = DigitalFilter(name)
                for i, val in enumerate(['base'] + data.values):
                    setattr(dlf, val, data()[i])
                dlf.factor = np.around([dlf.base[1] / dlf.base[0]], 15)
                FILTERS[ftype][name] = dlf
            return FILTERS[ftype][name]
        else:
            return object.__getattribute__(self, name)