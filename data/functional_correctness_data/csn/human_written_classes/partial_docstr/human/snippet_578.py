class CountryPower:
    """Class to hold information on the residential or electrical data of a
    country. Data from Wikipedia, obtained in 2017.

    Parameters
    ----------
    plugs : tuple(str)
        Tuple of residential plug letter codes in use in the country, [-]
    voltage : float or tuple(float)
        Voltage or voltages in common use of the country (residential data
        has one voltage; industrial data has multiple often), [V]
    freq : float
        The electrical frequency in use in the country, [Hz]
    country : str
        The name of the country, [-]
    """
    __slots__ = ('plugs', 'voltage', 'freq', 'country')

    def __repr__(self):
        return 'CountryPower(country="%s", voltage=%s, freq=%d, plugs=%s)' % (self.plugs, self.voltage, self.freq, self.country)

    def __init__(self, country, voltage, freq, plugs=None):
        self.plugs = plugs
        self.voltage = voltage
        self.freq = freq
        self.country = country