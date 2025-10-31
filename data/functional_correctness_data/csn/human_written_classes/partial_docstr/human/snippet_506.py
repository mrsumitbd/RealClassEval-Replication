import gpiod

class Chip:
    """Abstraction for handling all breaking changes over the lifecycle of gpiod"""
    _CONSUMER = 'adafruit_blinka'
    id: str = None
    num_lines: int

    def __init__(self, chip_id: str):
        self.id = chip_id
        path = f'/dev/gpiochip{self.id}'
        self._chip = gpiod.Chip(path)
        info = self._chip.get_info()
        self.num_lines = info.num_lines

    def __repr__(self):
        return self.id

    def __eq__(self, other):
        return self.id == other