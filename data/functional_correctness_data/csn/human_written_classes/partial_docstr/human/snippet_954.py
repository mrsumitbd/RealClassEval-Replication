class IncrementalEncoder:
    """IncrementalEncoder determines the relative rotational position based
    on two series of pulses."""

    def __init__(self, seesaw, encoder=0):
        """Create an IncrementalEncoder object associated with the given
        eesaw device."""
        self._seesaw = seesaw
        self._encoder = encoder

    @property
    def position(self):
        """The current position in terms of pulses. The number of pulses per
        rotation is defined by the specific hardware."""
        return self._seesaw.encoder_position(self._encoder)

    @position.setter
    def position(self, value):
        self._seesaw.set_encoder_position(value, self._encoder)