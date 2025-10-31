class ChannelIterator:
    """
    Iterator for generating and managing channel colors.

    This class provides a way to iterate through a sequence of channel colors,
    generating new colors in a visually distinct sequence when needed.
    """
    DEFAULT_COLORS = ['FF0000', '00FF00', '0000FF', 'FF00FF', '00FFFF', 'FFFF00', 'FFFFFF']

    def __init__(self, num_channels=0):
        """
        Initialize the channel iterator.

        Args:
            num_channels: Initial number of channels to pre-generate
        """
        self._channels = []
        self._current_index = 0
        self._generate_channels(num_channels)

    def _generate_channels(self, count):
        """Generate the specified number of unique channel colors."""
        for i in range(len(self._channels), count):
            if i < len(self.DEFAULT_COLORS):
                color = self.DEFAULT_COLORS[i]
            else:
                hue = int(i * 137.5 % 360)
                r, g, b = self._hsv_to_rgb(hue / 360.0, 1.0, 1.0)
                color = f'{int(r * 255):02X}{int(g * 255):02X}{int(b * 255):02X}'
            self._channels.append({'label': f'Channel {i + 1}', 'color': color})

    @staticmethod
    def _hsv_to_rgb(h, s, v):
        """Convert HSV color space to RGB color space."""
        h = h * 6.0
        i = int(h)
        f = h - i
        p = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))
        if i == 0:
            return (v, t, p)
        elif i == 1:
            return (q, v, p)
        elif i == 2:
            return (p, v, t)
        elif i == 3:
            return (p, q, v)
        elif i == 4:
            return (t, p, v)
        else:
            return (v, p, q)

    def __iter__(self):
        """Return the iterator object itself."""
        self._current_index = 0
        return self

    def __next__(self):
        """Return the next channel color."""
        if self._current_index >= len(self._channels):
            self._generate_channels(len(self._channels) + 1)
        if self._current_index < len(self._channels):
            result = self._channels[self._current_index]
            self._current_index += 1
            return result
        raise StopIteration

    def get_channel(self, index):
        """
        Get channel color by index.

        Args:
            index: Index of the channel to retrieve

        Returns:
            dict: Channel information with 'label' and 'color' keys
        """
        if index >= len(self._channels):
            self._generate_channels(index + 1)
        return self._channels[index]

    def __len__(self):
        """Return the number of generated channels."""
        return len(self._channels)