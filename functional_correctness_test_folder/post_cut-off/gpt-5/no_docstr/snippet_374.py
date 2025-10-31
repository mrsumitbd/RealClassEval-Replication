class ChannelIterator:

    def __init__(self, num_channels=0):
        self._channels = self._generate_channels(
            int(num_channels) if num_channels is not None else 0)
        self._iter_index = 0

    def _generate_channels(self, count):
        if count <= 0:
            return []
        channels = []
        for i in range(count):
            h = (i / float(count)) % 1.0
            s = 1.0
            v = 1.0
            channels.append(self._hsv_to_rgb(h, s, v))
        return channels

    @staticmethod
    def _hsv_to_rgb(h, s, v):
        if s <= 0.0:
            r = g = b = v
        else:
            h = (h % 1.0) * 6.0
            i = int(h)
            f = h - i
            p = v * (1.0 - s)
            q = v * (1.0 - s * f)
            t = v * (1.0 - s * (1.0 - f))
            i = i % 6
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
            else:
                r, g, b = v, p, q
        return (int(round(r * 255)), int(round(g * 255)), int(round(b * 255)))

    def __iter__(self):
        self._iter_index = 0
        return self

    def __next__(self):
        if self._iter_index >= len(self._channels):
            raise StopIteration
        value = self._channels[self._iter_index]
        self._iter_index += 1
        return value

    def get_channel(self, index):
        return self._channels[index]

    def __len__(self):
        return len(self._channels)
