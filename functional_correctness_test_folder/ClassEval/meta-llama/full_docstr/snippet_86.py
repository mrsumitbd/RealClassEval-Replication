
class Thermostat:
    """
    The class manages temperature control, including setting and retrieving the target temperature, adjusting the mode, and simulating temperature operation.
    """

    def __init__(self, current_temperature, target_temperature, mode):
        """
        initialize instances of the Thermostat class, including the current temperature, target temperature, and operating mode.
        :param current_temperature: float
        :param target_temperature: float
        :param mode: str, the work mode
        """
        self.current_temperature = current_temperature
        self.target_temperature = target_temperature
        self.mode = mode

    def get_target_temperature(self):
        """
        Get the target temperature of an instance of the Thermostat class.
        :return self.current_temperature: int
        >>> thermostat.get_target_temperature()
        37.5
        """
        return self.target_temperature

    def set_target_temperature(self, temperature):
        """
        Set the target temperature
        :param temperature: float, the target temperature
        >>> thermostat.set_target_temperature(37.6)
        >>> thermostat.target_temperature
        37.6
        """
        self.target_temperature = temperature

    def get_mode(self):
        """
        Get the current work mode
        :return mode: str, working mode. only ['heat', 'cool']
        """
        return self.mode

    def set_mode(self, mode):
        """
        Get the current work mode
        :param mode: str, working mode. only ['heat', 'cool']
        >>> thermostat.set_mode('cool')
        >>> thermostat.mode
        'cool'
        """
        if mode not in ['heat', 'cool']:
            raise ValueError("Invalid mode. Mode should be 'heat' or 'cool'.")
        self.mode = mode

    def auto_set_mode(self):
        """
        Automatically set the operating mode by comparing with the current temperature and target temperature. If the current temperature is lower than the target temperature, the operating mode is set to 'heat', otherwise it is set to 'cool'.
        >>> thermostat = Thermostat(20.4, 37.5, 'cool')
        >>> thermostat.auto_set_mode()
        >>> thermostat.mode
        'heat'
        """
        if self.current_temperature < self.target_temperature:
            self.mode = 'heat'
        else:
            self.mode = 'cool'

    def auto_check_conflict(self):
        """
        Check if there is a conflict between the operating mode and the relationship between the current temperature and the target temperature.
        If there is a conflict, the operating mode will be adjusted automatically.
        :return: True if mode isn't conflict with the relationship between the current temperature and the target temperature, or False otherwise.
        >>> thermostat = Thermostat(20.4, 37.5, 'cool')
        >>> thermostat.auto_check_conflict()
        False
        >>> thermostat.mode
        'heat'
        """
        if (self.mode == 'heat' and self.current_temperature >= self.target_temperature) or (self.mode == 'cool' and self.current_temperature <= self.target_temperature):
            self.auto_set_mode()
            return False
        return True

    def simulate_operation(self):
        """
        simulate the operation of Thermostat. It will automatically start the auto_set_mode method to set the operating mode,
        and then automatically adjust the current temperature according to the operating mode until the target temperature is reached.
        :return time: int, the time it took to complete the simulation.
        >>> thermostat = Thermostat(20.4, 37.5, 'cool')
        >>> thermostat.simulate_operation()
        18
        """
        self.auto_set_mode()
        time = 0
        while self.current_temperature != self.target_temperature:
            if self.mode == 'heat':
                self.current_temperature = min(
                    self.current_temperature + 1, self.target_temperature)
            else:
                self.current_temperature = max(
                    self.current_temperature - 1, self.target_temperature)
            time += 1
        return time


# Example usage:
if __name__ == "__main__":
    thermostat = Thermostat(20.4, 37.5, 'cool')
    print(thermostat.get_target_temperature())
    thermostat.set_target_temperature(37.6)
    print(thermostat.target_temperature)
    print(thermostat.get_mode())
    thermostat.set_mode('cool')
    print(thermostat.mode)
    thermostat.auto_set_mode()
    print(thermostat.mode)
    print(thermostat.auto_check_conflict())
    print(thermostat.mode)
    print(thermostat.simulate_operation())
