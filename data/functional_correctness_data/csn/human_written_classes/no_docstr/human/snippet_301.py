from packaging.version import Version
import pvlib
from functools import partial

class SAPM:

    def setup(self):
        set_weather_data(self)
        if Version(pvlib.__version__) >= Version('0.7.0'):
            kwargs = pvlib.temperature.TEMPERATURE_MODEL_PARAMETERS['sapm']
            kwargs = kwargs['open_rack_glass_glass']
            self.sapm_cell_wrapper = partial(pvlib.temperature.sapm_cell, **kwargs)
        else:
            sapm_celltemp = pvlib.pvsystem.sapm_celltemp

            def sapm_cell_wrapper(poa_global, temp_air, wind_speed):
                return sapm_celltemp(poa_global, wind_speed, temp_air)
            self.sapm_cell_wrapper = sapm_cell_wrapper

    def time_sapm_cell(self):
        self.sapm_cell_wrapper(self.poa, self.tamb, self.wind_speed)