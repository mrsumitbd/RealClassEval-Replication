
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
        self.weather_list = weather_list
        city_info = weather_list.get(self.city)
        if not city_info:
            self.temperature = None
            self.weather = None
            return (None, None)
        temp = city_info.get('temperature')
        weather = city_info.get('weather')
        temp_units = city_info.get('temperature units', 'celsius').lower()
        # Convert temperature if needed
        if tmp_units.lower() == temp_units:
            self.temperature = temp
        elif tmp_units.lower() == 'celsius' and temp_units == 'fahrenheit':
            self.temperature = (temp - 32) * 5 / 9
        elif tmp_units.lower() == 'fahrenheit' and temp_units == 'celsius':
            self.temperature = temp * 9 / 5 + 32
        else:
            self.temperature = temp  # fallback
        self.weather = weather
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
        return self.temperature * 9 / 5 + 32

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
        return (self.temperature - 32) * 5 / 9
