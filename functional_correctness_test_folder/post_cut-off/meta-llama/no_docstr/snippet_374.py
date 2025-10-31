
class ChannelIterator:

    def __init__(self, num_channels=0):
        self.num_channels = num_channels
        self.channels = self._generate_channels(num_channels)
        self.index = 0

    def _generate_channels(self, count):
        return [(i / count, 1, 1) for i in range(count)]

    @staticmethod
    def _hsv_to_rgb(h, s, v):
        h_i = int(h * 6)
        f = h * 6 - h_i
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)

        if h_i == 0:
            r, g, b = v, t, p
        elif h_i == 1:
            r, g, b = q, v, p
        elif h_i == 2:
            r, g, b = p, v, t
        elif h_i == 3:
            r, g, b = p, q, v
        elif h_i == 4:
            r, g, b = t, p, v
        elif h_i == 5:
            r, g, b = v, p, q

        return (int(r * 255), int(g * 255), int(b * 255))

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.channels):
            channel = self.channels[self.index]
            self.index += 1
            return self._hsv_to_rgb(*channel)
        else:
            raise StopIteration

    def get_channel(self, index):
        if index < len(self.channels):
            return self._hsv_to_rgb(*self.channels[index])
        else:
            raise IndexError("Index out of range")

    def __len__(self):
        return len(self.channels)
