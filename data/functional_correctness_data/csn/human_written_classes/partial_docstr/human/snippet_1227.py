from astropy.table import Table
import numpy as np

class Polarization:
    """
    Class for handling ACS polarization data. Input data for this class come from
    photometry of ACS polarization images. The methods associated with this class
    will transform the photometry into Stokes parameters and polarization properties,
    i.e., the polarization fraction and position angle.

    Parameters
    ----------
    pol0 : float
        Photometric measurement in POL0 filter. Units: electrons or electrons/second.
    pol60 : float
        Photometric measurement in POL60 filter. Units: electrons or electrons/second.
    pol120 : float
        Photometric measurement in POL120 filter. Units: electrons or electrons/second.
    filter_name : str
        Name of the filter crossed with the polarization filter, e.g., F606W.
    detector : {'wfc', 'hrc'}
        Name of the ACS detector used for the observation. Must be either WFC or HRC.
    pav3 : float or `~astropy.units.Quantity`
        Position angle of the HST V3 axis. This is stored in the ACS primary header under
        keyword PA_V3. Units: degrees.
    tables : `~acstools.polarization_tools.PolarizerTables`
        Object containing the polarization lookup tables containing the efficiency and
        transmission leak correction factors for the detectors and filters.

    Examples
    --------
    From an ACS/WFC F606W observation of Vela 1-81 (the polarized calibration standard
    star), we have count rates of 63684, 67420, and 63752 electrons/second in POL0V,
    POL60V, and POL120V, respectively. The PA_V3 keyword value in the image header is
    348.084 degrees. (Reference: Table 6; Cracraft & Sparks, 2007 (ACS ISR 2007-10)).
    In this simple case, we will use the polarization reference information contained
    in the acstools package for the calibration of the polarizers. We can use the
    Polarization class to determine the Stokes parameters and polarization properties
    as follows:

    >>> from acstools.polarization_tools import Polarization
    >>> vela_181 = Polarization(63684, 67420, 63752, 'F606W', 'WFC', 348.084)
    >>> vela_181.calc_stokes()
    >>> vela_181.calc_polarization()
    >>> print(f'I = {vela_181.stokes_i:.2f}, Q = {vela_181.stokes_q:.2f}, U = {vela_181.stokes_u:.2f}')
    I = 173336.09, Q = -3758.34, U = 9539.59

    >>> print(f'Polarization: {vela_181.polarization:.2%}, Angle: {vela_181.angle:.2f}')
    Polarization: 5.92%, Angle: 5.64 deg

    If we need to adjust the polarization calibration, we can do so by providing a
    different set of polarization tables using the `~acstools.polarization_tools.PolarizerTables`
    class. See the help text for that class for more information about input format.
    For the same source as above, we can explicitly provide the calibration tables
    (using the default tables in this example) as:

    >>> from acstools.polarization_tools import Polarization, PolarizerTables
    >>> vela_181 = Polarization(63684, 67420, 63752, 'F606W', 'WFC', 348.084,
    >>>                         tables=PolarizerTables.from_yaml('data/polarizer_tables.yaml'))
    >>> vela_181.calc_stokes()
    >>> vela_181.calc_polarization()
    >>> print(f'I = {vela_181.stokes_i:.2f}, Q = {vela_181.stokes_q:.2f}, U = {vela_181.stokes_u:.2f}')
    I = 173336.09, Q = -3758.34, U = 9539.59

    >>> print(f'Polarization: {vela_181.polarization:.2%}, Angle: {vela_181.angle:.2f}')
    Polarization: 5.92%, Angle: 5.64 deg
    """

    def __init__(self, pol0, pol60, pol120, filter_name, detector, pav3, tables=None):
        self.pol0 = pol0
        self.pol60 = pol60
        self.pol120 = pol120
        self.filter_name = filter_name.upper()
        self.detector = detector.lower()
        self.pav3 = pav3
        if self.detector not in ['wfc', 'hrc']:
            raise ValueError('Detector must be either WFC or HRC')
        self.stokes_i = None
        self.stokes_q = None
        self.stokes_u = None
        self.polarization = None
        self.angle = None
        tables = tables.data if tables else PolarizerTables.from_package_data().data
        if 'transmission' not in tables:
            raise KeyError('Missing polarization reference transmission table.')
        if 'efficiency' not in tables:
            raise KeyError('Missing polarization reference efficiency table.')
        try:
            leak_tab = Table(tables['transmission'][self.detector])
            eff_tab = Table(tables['efficiency'][self.detector])
        except KeyError:
            raise KeyError(f'Polarization reference tables may be missing information for detector {self.detector.upper()}.')
        try:
            self.transmission_correction = leak_tab[np.where(leak_tab['filter'] == self.filter_name)]['correction'][0]
        except IndexError:
            raise IndexError(f'No match found in input transmission leak correction table for detector {self.detector.upper()} and filter {self.filter_name}.')
        try:
            self.c0 = eff_tab[np.where(eff_tab['filter'] == filter_name.upper())]['pol0'][0]
            self.c60 = eff_tab[np.where(eff_tab['filter'] == filter_name.upper())]['pol60'][0]
            self.c120 = eff_tab[np.where(eff_tab['filter'] == filter_name.upper())]['pol120'][0]
        except IndexError:
            raise IndexError(f'No match found in input efficiency correction table for detector {self.detector.upper()} and filter {self.filter_name}.')

    def calc_stokes(self):
        """
        Calculate Stokes parameters using attributes set at initialization.
        """
        self.stokes_i, self.stokes_q, self.stokes_u = calc_stokes(self.pol0, self.pol60, self.pol120, c0=self.c0, c60=self.c60, c120=self.c120)

    def calc_polarization(self):
        """
        Calculate the polarization parameters (fractional polarization and position angle)
        using attributes set at initialization.
        """
        self.polarization = calc_fraction(self.stokes_i, self.stokes_q, self.stokes_u, transmission_correction=self.transmission_correction)
        self.angle = calc_theta(self.stokes_q, self.stokes_u, self.detector, self.pav3)