from dataclasses import dataclass
from pathlib import Path
from astropy.io import fits
from astromodels.utils import _get_data_file_path
from typing import List
import numpy as np

@dataclass(frozen=False)
class AbundanceTable:
    name: str
    tables: List[str]
    _current_table: str

    def set_table(self, table: str):
        """
        set the current table from AG89, WILM or ASPL

        :param table:
        :type table: str
        :returns:

        """
        old_table = self._current_table
        self._current_table = table
        if self.current_table not in self.tables:
            log.error(f"{self.name} does not contain {table} choose {','.join(self.table)}")
            self._current_table = old_table
            raise AssertionError()

    @property
    def current_table(self) -> str:
        convert = {'AG89': 'angr', 'ASPL': 'aspl', 'WILM': 'wilm'}
        return convert[self._current_table]

    @property
    def info(self) -> str:
        _abund_info = {}
        _abund_info['WILM'] = 'wilms\nfrom Wilms, Allen & McCray (2000), ApJ 542, 914 \n except for elements not listed which are given zero abundance)\n https://heasarc.nasa.gov/xanadu/xspec/manual/XSabund.html '
        _abund_info['AG89'] = 'angr\nfrom Anders E. & Grevesse N. (1989, Geochimica et Cosmochimica Acta 53, 197)\n https://heasarc.nasa.gov/xanadu/xspec/manual/XSabund.html'
        _abund_info['ASPL'] = 'aspl\nfrom Asplund M., Grevesse N., Sauval A.J. & Scott P. (2009, ARAA, 47, 481)\nhttps://heasarc.nasa.gov/xanadu/xspec/manual/XSabund.html'
        return _abund_info[self._current_table]

    @property
    def xsect_table(self) -> np.ndarray:
        """
        returns the XSECT table for the current model

        :returns:

        """
        _path: Path = Path('xsect') / f'xsect_{self.name}_{self.current_table}.fits'
        path_to_xsect: Path = _get_data_file_path(_path)
        with fits.open(path_to_xsect) as fxs:
            dxs = fxs[1].data
            xsect_ene = dxs['ENERGY']
            xsect_val = dxs['SIGMA']
        return (np.array(xsect_ene, dtype=np.float64), np.array(xsect_val, dtype=np.float64))