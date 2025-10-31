class Pin:
    """A basic Pin class for use with Binho Nova."""
    IN = 'DIN'
    OUT = 'DOUT'
    AIN = 'AIN'
    AOUT = 'AOUT'
    PWM = 'PWM'
    LOW = 0
    HIGH = 1
    _nova = None

    def __init__(self, pin_id=None):
        if not Pin._nova:
            from adafruit_blinka.microcontroller.nova import Connection
            Pin._nova = Connection.getInstance()
        if pin_id > 4:
            raise ValueError('Invalid pin {}.'.format(pin_id))
        self.id = pin_id

    def init(self, mode=IN, pull=None):
        """Initialize the Pin"""
        if self.id is None:
            raise RuntimeError('Can not init a None type pin.')
        if pull:
            raise ValueError('Internal pull up/down not currently supported.')
        Pin._nova.setIOpinMode(self.id, mode)

    def value(self, val=None):
        """Set or return the Pin Value"""
        if self.id is None:
            raise RuntimeError('Can not access a None type pin.')
        if val is None:
            return int(Pin._nova.getIOpinValue(self.id).split('VALUE ')[1])
        if val in (self.LOW, self.HIGH):
            Pin._nova.setIOpinValue(self.id, val)
            return None
        raise RuntimeError('Invalid value for pin')