class ChannelIterator:
    '''
    Iterator for generating and managing channel colors.
    This class provides a way to iterate through a sequence of channel colors,
    generating new colors in a visually distinct sequence when needed.
    '''

    def __init__(self, num_channels=0):
        '''
        Initialize the channel iterator.
        Args:
            num_channels: Initial number of channels to pre-generate
        '''
        if num_channels is None:
            num_channels = 0
        if not isinstance(num_channels, int) or num_channels < 0:
            raise ValueError("num_channels must be a non-negative integer")

        self._channels = []
        self._iter_index = 0
        self._created = 0
        self._hue = 0.0  # running hue in [0,1)
        self._golden = 0.618033988749895  # golden ratio conjugate for good spacing
        self._levels = [
            (0.70, 0.95),
            (0.80, 0.85),
            (0.85, 0.78),
            (0.65, 0.88),
        ]

        if num_channels > 0:
            self._generate_channels(num_channels)

    def _generate_channels(self, count):
        '''Generate the specified number of unique channel colors.'''
        if count <= 0:
            return
        for _ in range(int(count)):
            # advance hue using golden ratio conjugate for blue-noise-like distribution
            self._hue = (self._hue + self._golden) % 1.0
            s, v = self._levels[self._created % len(self._levels)]
            r, g, b = self._hsv_to_rgb(self._hue, s, v)
            label = f"Channel {self._created + 1}"
            self._channels.append({'label': label, 'color': (r, g, b)})
            self._created += 1

    @staticmethod
    def _hsv_to_rgb(h, s, v):
        '''Convert HSV color space to RGB color space.'''
        if s <= 0.0:
            r = g = b = int(round(v * 255))
            return r, g, b

        h = float(h) % 1.0
        s = max(0.0, min(1.0, float(s)))
        v = max(0.0, min(1.0, float(v)))

        h6 = h * 6.0
        i = int(h6)  # sector 0..5
        f = h6 - i
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

        return int(round(r * 255)), int(round(g * 255)), int(round(b * 255))

    def __iter__(self):
        '''Return the iterator object itself.'''
        return self

    def __next__(self):
        '''Return the next channel color.'''
        if self._iter_index >= len(self._channels):
            self._generate_channels(1)
        item = self._channels[self._iter_index]
        self._iter_index += 1
        return item

    def get_channel(self, index):
        '''
        Get channel color by index.
        Args:
            index: Index of the channel to retrieve
        Returns:
            dict: Channel information with 'label' and 'color' keys
        '''
        if not isinstance(index, int):
            raise TypeError("index must be an integer")
        if index < 0:
            raise IndexError("index must be non-negative")
        if index >= len(self._channels):
            self._generate_channels(index + 1 - len(self._channels))
        return self._channels[index]

    def __len__(self):
        '''Return the number of generated channels.'''
        return len(self._channels)
