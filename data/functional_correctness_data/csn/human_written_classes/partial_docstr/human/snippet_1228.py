from astropy.table import Table
from astropy.utils.data import get_pkg_data_filename
import os
import yaml

class PolarizerTables:
    """
    A class for holding all of the polarization tables (as astropy tables) in attributes.
    These attributes are:

    * wfc_transmission: Transmission and leak correction factors for computing ACS/WFC fractional polarization.
    * hrc_transmission: Transmission and leak correction factors for computing ACS/HRC fractional polarization.
    * wfc_efficiency: Efficiencies of the ACS/WFC polarizers for computing Stokes parameters.
    * hrc_efficiency: Efficiencies of the ACS/HRC polarizers for computing Stokes parameters.

    .. note::
        The default table contained within the acstools package uses average transmission leak correction terms
        for a source with a spectrum flat in wavelength space.

    Polarizer calibration information can be read from the default YAML file contained in the
    acstools package, or from a user-supplied YAML file using the class methods :meth:`from_yaml` and
    :meth:`from_package_data`. The YAML file format is:

    .. code-block:: yaml

        transmission:
            meta: dictionary of metadata
            detector:
                filter: list of ACS filters
                t_para: list of parallel transmissions for each filter
                t_perp: list of perpendicular transmissions for each filter
                correction: list of transmission leak correction factors for each filter
        efficiency:
            meta: dictionary of metadata
            detector:
                filter: list of ACS filters
                pol0: list of POL0 coefficients matching each filter
                pol60: list of POL60 coefficients matching each filter
                pol120: list of POL120 coefficients matching each filter

    The meta elements will pass a dictionary of metadata to the output tables. Any metadata
    can be included, but at minimum a description of the origin of the table values should
    be provided. Multiple detectors can be contained in a single YAML file. An example is
    shown below:

    .. code-block:: yaml

        transmission:
            meta: {'description': 'Descriptive message.'}
            wfc:
                filter: ['F475W', 'F606W']
                t_para: [0.42, 0.51]
                t_perp: [0.0, 0.0]
                correction: [1.0, 1.0]
            hrc:
                filter: ['F330W']
                t_para: [0.48]
                t_perp: [0.05]
                correction: [1.21]
        efficiency:
            meta: {'description': 'Descriptive message.'}
            wfc:
                filter: ['F475W', 'F606W']
                pol0: [1.43, 1.33]
                pol60: [1.47, 1.36]
                pol120: [1.42, 1.30]
            hrc:
                filter: ['F330W']
                pol0: [1.73]
                pol60: [1.53]
                pol120: [1.64]

    Parameters
    ----------
    input_dict : dict

    Examples
    --------

    To use the default values supplied in the acstools package (which come from the ACS
    Data Handbook section 5.3):

    >>> from acstools.polarization_tools import PolarizerTables
    >>> tables = PolarizerTables.from_package_data()
    >>> print(tables.wfc_efficiency)
    filter  pol0  pol60  pol120
    ------ ------ ------ ------
     F475W 1.4303 1.4717 1.4269
     F606W 1.3314 1.3607 1.3094
     F775W 0.9965 1.0255 1.0071

    To supply your own YAML file of the appropriate format:

    >>> from acstools.polarization_tools import PolarizerTables
    >>> tables = PolarizerTables.from_yaml('data/polarizer_tables.yaml')
    >>> print(tables.wfc_transmission)
    filter       t_para               t_perp             correction
    ------ ------------------ ---------------------- ------------------
    F475W 0.4239276798513098 0.00015240583841551956  1.000719276691027
    F606W 0.5156734594049419 5.5908749369641956e-05  1.000216861312415
    F775W 0.6040891283746557    0.07367364117759412 1.2777959654493372

    >>> print(tables.wfc_transmission.meta['description'])
    WFC filters use MJD corresponding to 2020-01-01. HRC filters use MJD corresponding to 2007-01-01.
    """

    def __init__(self, input_dict):
        self.data = input_dict
        self.wfc_transmission = Table(self.data['transmission']['wfc'], names=('filter', 't_para', 't_perp', 'correction'), meta=self.data['transmission']['meta'])
        self.hrc_transmission = Table(self.data['transmission']['hrc'], names=('filter', 't_para', 't_perp', 'correction'), meta=self.data['transmission']['meta'])
        self.wfc_efficiency = Table(self.data['efficiency']['wfc'], names=('filter', 'pol0', 'pol60', 'pol120'), meta=self.data['efficiency']['meta'])
        self.hrc_efficiency = Table(self.data['efficiency']['hrc'], names=('filter', 'pol0', 'pol60', 'pol120'), meta=self.data['efficiency']['meta'])

    @classmethod
    def from_yaml(cls, yaml_file):
        """
        Read in a YAML file containing polarizer calibration data.

        Parameters
        ----------
        yaml_file : str
            Path to the YAML file containing the polarizer calibration information.

        Returns
        -------
        pol_tables : `~acstools.polarizer_tools.PolarizerTables`
        """
        with open(yaml_file, 'r') as yf:
            input_dict = yaml.safe_load(yf)
        return cls(input_dict)

    @classmethod
    def from_package_data(cls):
        """
        Use the YAML file contained within the acstools package to retrieve the polarizer
        calibration data.

        Returns
        -------
        pol_tables : `~acstools.polarizer_tools.PolarizerTables`
        """
        filename = get_pkg_data_filename(os.path.join('data', 'polarizer_tables.yaml'))
        return cls.from_yaml(filename)