import datetime
from pvlib import solarposition

class SolarPositionCalcTime:

    def setup(self):
        self.start = datetime.datetime(2020, 9, 14, 12)
        self.end = datetime.datetime(2020, 9, 14, 15)
        self.value = 0.05235987755982988
        self.lat = 32.2
        self.lon = -110.9
        self.attribute = 'alt'

    def time_calc_time(self):
        solarposition.calc_time(self.start, self.end, self.lat, self.lon, self.attribute, self.value)