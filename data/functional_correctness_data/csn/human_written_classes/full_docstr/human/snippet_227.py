import numpy as np
import h5py
from dataclasses import dataclass
import collections
from typing import Dict, List, Optional, Union

@dataclass
class TemplateFile:
    """
    simple container to read and write
    the data to an hdf5 file

    """
    name: str
    description: str
    grid: np.ndarray
    parameters: Dict[str, np.ndarray]
    parameter_order: List[str]
    energies: np.ndarray
    interpolation_degree: int
    spline_smoothing_factor: float

    def save(self, file_name: str):
        """
        serialize the contents to a file

        :param file_name:
        :type file_name: str
        :returns:

        """
        with h5py.File(file_name, 'w') as f:
            f.attrs['name'] = self.name
            f.attrs['description'] = self.description
            f.attrs['interpolation_degree'] = self.interpolation_degree
            f.attrs['spline_smoothing_factor'] = self.spline_smoothing_factor
            f.create_dataset('energies', data=self.energies, compression='gzip')
            f.create_dataset('grid', data=self.grid, compression='gzip')
            dt = h5py.special_dtype(vlen=str)
            po = np.array(self.parameter_order, dtype=dt)
            f.create_dataset('parameter_order', data=po)
            par_group = f.create_group('parameters')
            for k in self.parameter_order:
                par_group.create_dataset(k, data=self.parameters[k], compression='gzip')

    @classmethod
    def from_file(cls, file_name: str):
        """
        read contents from a file

        :param cls:
        :type cls:
        :param file_name:
        :type file_name: str
        :returns:

        """
        with h5py.File(file_name, 'r') as f:
            name = f.attrs['name']
            description = f.attrs['description']
            interpolation_degree = f.attrs['interpolation_degree']
            spline_smoothing_factor = f.attrs['spline_smoothing_factor']
            energies = f['energies'][()]
            parameter_order = f['parameter_order'][()]
            grid = f['grid'][()]
            parameters = collections.OrderedDict()
            for k in parameter_order:
                parameters[k] = f['parameters'][k][()]
        return cls(name=name, description=description, interpolation_degree=interpolation_degree, spline_smoothing_factor=spline_smoothing_factor, energies=energies, parameter_order=parameter_order, parameters=parameters, grid=grid)