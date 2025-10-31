import pvlib
from packaging.version import Version

class Fuentes:

    def setup(self):
        if Version(pvlib.__version__) < Version('0.8.0'):
            raise NotImplementedError
        set_weather_data(self)

    def time_fuentes(self):
        pvlib.temperature.fuentes(self.poa, self.tamb, self.wind_speed, noct_installed=45)