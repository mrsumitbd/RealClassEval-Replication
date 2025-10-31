
class ChannelIterator:
    def __init__(self, num_channels=0):
        self._channels = self._generate_channels(num_channels)
        self._index = 0

    def _generate_channels(self, count):
        """Generate `count` distinct RGB channels evenly spaced in HSV hue."""
        channels = []
        if count <= 0:
            return channels
        # Evenly space hue values from 0 to 360 (exclusive)
        step = 360.0 / count
        for i in range(count):
            h = (i * step) % 360
            s = 1.0
            v = 1.0
            channels.append(self._hsv_to_rgb(h, s, v))
        return channels

    @staticmethod
    def _hsv_to_rgb(h, s, v):
        """Convert HSV (h in degrees 0-360, s and v in 0-1) to RGB tuple (0-255)."""
        h = float(h)
        s = float(s)
        v = float(v)
        if s == 0.0:
            r = g = b = int(v * 255)
            return (r, g, b)
        h /= 60.0  # sector 0 to 5
        i = int(h)
        f = h - i
        p = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))
        if i == 0:
            r, g, b = v, t, p
        elif i == 1:
            r, g, b = q, v, p
        elif i == 2:
            r, g, b = p, v, t
        elif i == 3:
            r, g, b = p, q, v
        elif i == 4:
            r, g, b = t, p, v
        else:  # i == 5
            r, g, b = v, p, q
        return (int(r * 255), int(g * 255), int(b * 255))

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._channels):
            raise StopIteration
        channel = self._channels[self._index]
        self._index += 1
        return channel

    def get_channel(self, index):
        if not 0 <= index < len(self._channels):
            raise IndexError("Channel index out of range")
        return self._channels[index]

    def __len__(self):
        return len(self._channels)
