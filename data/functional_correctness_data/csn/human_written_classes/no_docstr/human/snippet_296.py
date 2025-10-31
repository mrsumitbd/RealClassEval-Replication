class Location:

    def setup(self):
        set_solar_position(self)

    def time_location_get_airmass(self):
        self.location.get_airmass(solar_position=self.solar_position)

    def time_location_get_solarposition(self):
        self.location.get_solarposition(times=self.times)

    def time_location_get_clearsky(self):
        self.location.get_clearsky(times=self.times, solar_position=self.solar_position)