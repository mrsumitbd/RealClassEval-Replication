class AttenuatorPath:
    """A convenience class that allows users to control each attenuator path
    separately as different objects, as opposed to passing in an index number
    to the functions of an attenuator device object.

    This decouples the test code from the actual attenuator device used in the
    physical test bed.

    For example, if a test needs to attenuate four signal paths, this allows the
    test to do:

    .. code-block:: python

        self.attenuation_paths[0].set_atten(50)
        self.attenuation_paths[1].set_atten(40)

    instead of:

    .. code-block:: python

        self.attenuators[0].set_atten(0, 50)
        self.attenuators[0].set_atten(1, 40)

    The benefit the former is that the physical test bed can use either four
    single-channel attenuators, or one four-channel attenuators. Whereas the
    latter forces the test bed to use a four-channel attenuator.
    """

    def __init__(self, attenuation_device, idx=0, name=None):
        self.model = attenuation_device.model
        self.attenuation_device = attenuation_device
        self.idx = idx
        self.name = name
        if self.idx >= attenuation_device.path_count:
            raise IndexError('Attenuator index out of range!')

    def set_atten(self, value):
        """This function sets the attenuation of Attenuator.

        Args:
            value: This is a floating point value for nominal attenuation to be
                set. Unit is db.
        """
        self.attenuation_device.set_atten(self.idx, value)

    def get_atten(self):
        """Gets the current attenuation setting of Attenuator.

        Returns:
            A float that is the current attenuation value. Unit is db.
        """
        return self.attenuation_device.get_atten(self.idx)

    def get_max_atten(self):
        """Gets the max attenuation supported by the Attenuator.

        Returns:
            A float that is the max attenuation value.
        """
        return self.attenuation_device.max_atten