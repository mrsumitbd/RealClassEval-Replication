class TextLevelMeter:
    """
    TODO: Fix DocTest:

    >> tl = TextLevelMeter(255, 9)
    >> tl.feed(0)
    '|   *   |'
    >> tl.feed(128)
    '|   | * |'
    >> tl.feed(255)
    '|   |  *|'
    >> tl.feed(-128)
    '| * |   |'
    >> tl.feed(-255)
    '|*  |   |'

    >> tl = TextLevelMeter(255, 74)
    >> tl.feed(0)
    '|                                   *                                   |'
    >> tl.feed(128)
    '|                                   |                 *                 |'
    >> tl.feed(255)
    '|                                   |                                  *|'
    >> tl.feed(-128)
    '|                 *                 |                                   |'
    >> tl.feed(-255)
    '|*                                  |                                   |'
    """

    def __init__(self, max_value, width):
        self.max_value = max_value
        fill_len = int(round((width - 3) / 2))
        fill = ' ' * fill_len
        self.source_msg = '|' + fill + '|' + fill + '|'
        self.offset = fill_len + 1
        self.max_width = fill_len

    def feed(self, value):
        value = int(round(float(value) / self.max_value * self.max_width + self.offset))
        return self.source_msg[:value] + '*' + self.source_msg[value + 1:]