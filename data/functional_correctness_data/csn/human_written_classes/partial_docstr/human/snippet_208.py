from typing import Iterable

class BackendMapping:
    """
    A two-way, non-unique dict-like mapping between keys used to set
    the matplotlib plotting backend in Python and IPython environments.
    Primarily used by `as_python()` and `as_ipython()` methods of
    `HypertoolsBackend`.  Funnels multiple equivalent keys within the
    same interpreter (Python vs. IPython) to a "default", then maps
    between that and the analog from the other interpreter type. At
    either step, a key with no corresponding value returns the key (see
    `ParrotDict` docstring for more info).
    """

    def __init__(self, _dict):
        self.py_to_ipy = ParrotDict()
        self.ipy_to_py = ParrotDict()
        self.equivalents = ParrotDict()
        for py_key, ipy_key in _dict.items():
            py_key_default = self._store_equivalents(py_key)
            ipy_key_default = self._store_equivalents(ipy_key)
            self.py_to_ipy[py_key_default] = ipy_key_default
            self.ipy_to_py[ipy_key_default] = py_key_default

    def _store_equivalents(self, keylist):
        if not isinstance(keylist, str) and isinstance(keylist, Iterable):
            default_key = keylist[0]
            for key_equiv in keylist[1:]:
                self.equivalents[key_equiv] = default_key
        else:
            default_key = keylist
        return default_key