class SensorFactory:
    """Given a sensor definition, constructs the appropriate HolodeckSensor object."""

    @staticmethod
    def _default_name(sensor_class):
        return sensor_class.sensor_type

    @staticmethod
    def build_sensor(client, sensor_def):
        """Constructs a given sensor associated with client

        Args:
            client (:obj:`str`): Name of the agent this sensor is attached to
            sensor_def (:class:`SensorDefinition`): Sensor definition to construct

        Returns:

        """
        if sensor_def.sensor_name is None:
            sensor_def.sensor_name = SensorFactory._default_name(sensor_def.type)
        return sensor_def.type(client, sensor_def.agent_name, sensor_def.agent_type, sensor_def.sensor_name, config=sensor_def.config)