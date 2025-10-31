class Sieve:
    """Class for storing data on sieves. If a property is not available, it is
    set to None.

    Attributes
    ----------
    designation : str
        The standard name of the sieve - its opening's length in units of
        millimeters
    old_designation : str
        The older, imperial-esque name of the sieve; in Numbers, or inches for
        large sieves
    opening : float
        The opening length of the sieve holes, [m]
    opening_inch : float
        The opening length of the sieve holes in the rounded inches as stated
        in common tables (not exactly equal to the `opening`), [inch]
    Y_variation_avg : float
        The allowable average variation in the Y direction of the sieve
        openings, [m]
    X_variation_max : float
        The allowable maximum variation in the X direction of the sieve
        openings, [m]
    max_opening : float
        The maximum allowable opening of the sieve, [m]
    calibration_samples : float
        The number of opening sample inspections required for `calibration`-
        type sieve openings (per 100 ft^2 of sieve material), [1/(ft^2)]
    compliance_sd : float
        The maximum standard deviation of `compliance`-type sieve openings,
        [-]
    inspection_samples : float
        The number of opening sample inspections required for `inspection`-
        type sieve openings (based on an 8-inch sieve), [-]
    inspection_sd : float
        The maximum standard deviation of `inspection`-type sieve openings,
        [-]
    calibration_samples : float
        The number of opening sample inspections required for `calibration`-
        type sieve openings (based on an 8-inch sieve), [-]
    calibration_sd : float
        The maximum standard deviation of `calibration`-type sieve openings,
        [-]
    d_wire : float
        Typical wire diameter of the specified sieve size, [m]
    d_wire_min : float
        Permissible minimum wire diameter of specified sieve size, [m]
    d_wire_max : float
        Permissible maximum wire diameter of specified sieve size, [m]

    """
    __slots__ = ('designation', 'old_designation', 'opening', 'opening_inch', 'Y_variation_avg', 'X_variation_max', 'max_opening', 'calibration_samples', 'compliance_sd', 'inspection_samples', 'inspection_sd', 'calibration_samples', 'calibration_sd', 'd_wire', 'd_wire_min', 'd_wire_max', 'compliance_samples')

    def __repr__(self):
        return f'<Sieve, designation {self.designation} mm, opening {self.opening:g} m>'

    def __init__(self, designation, old_designation=None, opening=None, opening_inch=None, Y_variation_avg=None, X_variation_max=None, max_opening=None, compliance_samples=None, compliance_sd=None, inspection_samples=None, inspection_sd=None, calibration_samples=None, calibration_sd=None, d_wire=None, d_wire_min=None, d_wire_max=None):
        self.designation = designation
        self.old_designation = old_designation
        self.opening_inch = opening_inch
        self.opening = opening
        self.Y_variation_avg = Y_variation_avg
        self.X_variation_max = X_variation_max
        self.max_opening = max_opening
        self.compliance_samples = compliance_samples
        self.compliance_sd = compliance_sd
        self.inspection_samples = inspection_samples
        self.inspection_sd = inspection_sd
        self.calibration_samples = calibration_samples
        self.calibration_sd = calibration_sd
        self.d_wire = d_wire
        self.d_wire_min = d_wire_min
        self.d_wire_max = d_wire_max