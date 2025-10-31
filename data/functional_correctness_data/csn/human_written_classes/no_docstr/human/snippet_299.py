from pvlib import solarposition
import pandas as pd

class SolarPositionNumba:
    params = [1, 10, 100]
    param_names = ['ndays']

    def setup(self, ndays):
        self.times = pd.date_range(start='20180601', freq='1min', periods=1440 * ndays)
        self.times_localized = self.times.tz_localize('Etc/GMT+7')
        self.lat = 35.1
        self.lon = -106.6
        self.times_daily = pd.date_range(start='20180601', freq='24h', periods=ndays, tz='Etc/GMT+7')

    def time_spa_python(self, ndays):
        solarposition.spa_python(self.times_localized, self.lat, self.lon, how='numba')

    def time_sun_rise_set_transit_spa(self, ndays):
        sun_rise_set_transit_spa(self.times_daily, self.lat, self.lon, how='numba')