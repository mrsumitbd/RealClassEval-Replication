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
        self._channels = []
        self._iter_index = 0
        self._hue = 0.0
        self._golden_ratio_conjugate = 0.618033988749895
        self._saturation = 0.65
        self._value = 0.95
        if num_channels > 0:
            self._generate_channels(num_channels)

    def _generate_channels(self, count):
        '''Generate the specified number of unique channel colors.'''
        for _ in range(max(0, count)):
            # Advance hue using golden ratio conjugate for visually distinct colors
            self._hue = (self._hue + self._golden_ratio_conjugate) % 1.0
            r, g, b = self._hsv_to_rgb(
                self._hue, self._saturation, self._value)
            label = f"Channel {len(self._channels) + 1}"
            self._channels.append({
                'label': label,
                'color': (r, g, b)
            })

    @staticmethod
    def _hsv_to_rgb(h, s, v):
        '''Convert HSV color space to RGB color space.'''
        if s == 0.0:
            r = g = b = int(round(v * 255))
            return r, g, b

        h = (h % 1.0) * 6.0
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
        if index < 0:
            raise IndexError("Channel index must be non-negative")
        if index >= len(self._channels):
            self._generate_channels(index + 1 - len(self._channels))
        return self._channels[index]

    def __len__(self):
        '''Return the number of generated channels.'''
        return len(self._channels)
