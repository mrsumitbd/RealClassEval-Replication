class PotentialParameter:
    """A class for defining parameters needed by the potential classes

    Parameters
    ----------
    name : str
        The name of the parameter. For example, "m" for mass.
    physical_type : str (optional)
        The physical type (as defined by `astropy.units`) of the expected
        physical units that this parameter is in. For example, "mass" for a mass
        parameter. Pass `None` if the parameter is not meant to be a Quantity (e.g.,
        string or integer values).
    default : numeric, str, array (optional)
        The default value of the parameter.
    equivalencies : `astropy.units.equivalencies.Equivalency` (optional)
        Any equivalencies required for the parameter.
    python_only : bool (optional)
        Controls whether to pass this parameter value to the C/Cython layer. True means
        a parameter is a Python-only value and will not be passed to the C/Cython layer.
        Default is False, meaning by default parameters will be passed to the C/Cython
        layer.
    """

    def __init__(self, name, physical_type='dimensionless', default=None, equivalencies=None, python_only=False):
        self.name = str(name)
        self.physical_type = str(physical_type) if physical_type is not None else None
        self.default = default
        self.equivalencies = equivalencies
        self.python_only = bool(python_only)

    def __repr__(self):
        if self.physical_type is None:
            return f'<PotentialParameter: {self.name}>'
        return f'<PotentialParameter: {self.name} [{self.physical_type}]>'