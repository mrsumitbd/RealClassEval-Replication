class IntegratedSurfaceDatabaseStation:
    """Class to hold data on a weather station in the Integrated Surface
    Database.

    License information for the database can be found at the following link:
    https://data.noaa.gov/dataset/global-surface-summary-of-the-day-gsod

    Note: Of the 28000 + stations in the database, approximately 3000 have WBAN
    identifiers; 26000 have unique names; 24000 have USAF identifiers; and
    there are only 25800 unique lat/lon pairs.

    To uniquely represent a weather station, a combination of identifiers
    must be used. (Name, USAF, WBAN) makes a good choice.

    Parameters
    ----------
    USAF : str or None if unassigned
        Air Force station ID. May contain a letter in the first position.
    WBAN : str or None if unassigned
        NCDC WBAN number
    NAME : str
        Name of the station; ex. 'CENTRAL COLORADO REGIONAL AP'
    CTRY : str or None if unspecified
        FIPS country ID
    ST : str or None if not in the US
        State for US stations
    ICAO : str or None if not an airport
        ICAO airport code
    LAT : float
        Latitude with a precision of one thousandths of a decimal degree,
        [degrees]
    LON : float
        Longitude with a precision of one thousandths of a decimal degree,
        [degrees]
    ELEV : float
        Elevation of weather station, [m]
    BEGIN : float
        Beginning Period Of Record (YYYYMMDD). There may be reporting gaps
        within the P.O.R.
    END : Ending Period Of Record (YYYYMMDD). There may be reporting gaps
        within the P.O.R.
    """
    __slots__ = ['USAF', 'WBAN', 'NAME', 'CTRY', 'ST', 'ICAO', 'LAT', 'LON', 'ELEV', 'BEGIN', 'END', 'raw_data', 'parsed_data']

    def __repr__(self):
        s = '<Weather station registered in the Integrated Surface Database, name %s, country %s, USAF %s, WBAN %s, coords (%s, %s) Weather data from %s to %s>'
        return s % (self.NAME, self.CTRY, self.USAF, self.WBAN, self.LAT, self.LON, str(self.BEGIN)[0:4], str(self.END)[0:4])

    def __init__(self, USAF, WBAN, NAME, CTRY, ST, ICAO, LAT, LON, ELEV, BEGIN, END):
        try:
            self.USAF = int(USAF)
        except:
            self.USAF = USAF
        self.WBAN = WBAN
        self.NAME = NAME
        self.CTRY = CTRY
        self.ST = ST
        self.ICAO = ICAO
        self.LAT = LAT
        self.LON = LON
        self.ELEV = ELEV
        self.BEGIN = int(BEGIN)
        self.END = int(END)