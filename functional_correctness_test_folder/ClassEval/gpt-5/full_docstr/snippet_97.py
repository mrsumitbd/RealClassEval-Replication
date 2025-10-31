class WeatherSystem:
    """
    This is a class representing a weather system that provides functionality to query weather information for a specific city and convert temperature units between Celsius and Fahrenheit.
    """

    def __init__(self, city) -> None:
        """
        Initialize the weather system with a city name.
        """
        self.temperature = None
        self.weather = None
        self.city = city
        self.weather_list = {}

    def query(self, weather_list, tmp_units='celsius'):
        """
        Query the weather system for the weather and temperature of the city,and convert the temperature units based on the input parameter.
        :param weather_list: a dictionary of weather information for different cities,dict.
        :param tmp_units: the temperature units to convert to, str.
        :return: the temperature and weather of the city, tuple.
        >>> weatherSystem = WeatherSystem('New York')
        >>> weather_list = {'New York': {'weather': 'sunny','temperature': 27,'temperature units': 'celsius'},'Beijing': {'weather': 'cloudy','temperature': 23,'temperature units': 'celsius'}}
        >>> weatherSystem.query(weather_list)
        (27, 'sunny')

        """
        self.weather_list = weather_list or {}
        city_info = self.weather_list.get(self.city)
        if not city_info or 'temperature' not in city_info or 'weather' not in city_info:
            self.temperature = None
            self.weather = None
            return (None, None)

        source_temp = city_info.get('temperature')
        source_units = str(city_info.get(
            'temperature units', 'celsius')).strip().lower()
        target_units = str(tmp_units).strip().lower()

        if source_units not in ('celsius', 'fahrenheit'):
            source_units = 'celsius'
        if target_units not in ('celsius', 'fahrenheit'):
            target_units = source_units

        temp = float(source_temp)
        if source_units == 'celsius' and target_units == 'fahrenheit':
            temp = (temp * 9.0 / 5.0) + 32.0
        elif source_units == 'fahrenheit' and target_units == 'celsius':
            temp = (temp - 32.0) * 5.0 / 9.0

        self.temperature = temp
        self.weather = city_info.get('weather')
        return (self.temperature, self.weather)

    def set_city(self, city):
        """
        Set the city of the weather system.
        :param city: the city to set, str.
        :return: None
        >>> weatherSystem = WeatherSystem('New York')
        >>> weatherSystem.set_city('Beijing')
        >>> weatherSystem.city
        'Beijing'

        """
        self.city = city

    def celsius_to_fahrenheit(self):
        """
        Convert the temperature from Celsius to Fahrenheit.
        :return: the temperature in Fahrenheit, float.
        >>> weatherSystem = WeatherSystem('New York')
        >>> weatherSystem.temperature = 27
        >>> weatherSystem.celsius_to_fahrenheit()
        80.6

        """
        if self.temperature is None:
            return None
        return (float(self.temperature) * 9.0 / 5.0) + 32.0

    def fahrenheit_to_celsius(self):
        """
        Convert the temperature from Fahrenheit to Celsius.
        :return: the temperature in Celsius, float.
        >>> weatherSystem = WeatherSystem('New York')
        >>> weatherSystem.temperature = 80.6
        >>> weatherSystem.fahrenheit_to_celsius()
        26.999999999999996

        """
        if self.temperature is None:
            return None
        return (float(self.temperature) - 32.0) * 5.0 / 9.0
