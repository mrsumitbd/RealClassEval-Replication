import pvlib
from packaging.version import Version

class Location_0_6_1:

    def setup(self):
        if Version(pvlib.__version__) < Version('0.6.1'):
            raise NotImplementedError
        set_solar_position(self)

    def time_location_get_sun_rise_set_transit_pyephem(self):
        self.location.get_sun_rise_set_transit(times=self.days, method='pyephem')

    def time_location_get_sun_rise_set_transit_spa(self):
        self.location.get_sun_rise_set_transit(times=self.days, method='spa')