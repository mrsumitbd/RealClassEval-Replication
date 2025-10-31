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
        self._phi = 0.6180339887498949  # golden ratio conjugate for good hue distribution
        self._h = 0.0  # hue seed in [0, 1)
        if num_channels and num_channels > 0:
            self._generate_channels(int(num_channels))

    def _generate_channels(self, count):
        '''Generate the specified number of unique channel colors.'''
        count = int(count)
        if count <= 0:
            return
        for _ in range(count):
            # advance hue using golden ratio to spread colors
            self._h = (self._h + self._phi) % 1.0
            idx = len(self._channels)
            variant = idx % 3
            s_values = [0.65, 0.80, 0.55]
            v_values = [0.95, 0.85, 0.75]
            s = s_values[variant]
            v = v_values[variant]
            r, g, b = self._hsv_to_rgb(self._h, s, v)
            label = f'CH{idx + 1}'
            self._channels.append({'label': label, 'color': (r, g, b)})

    @staticmethod
    def _hsv_to_rgb(h, s, v):
        '''Convert HSV color space to RGB color space.'''
        h = float(h) % 1.0
        s = max(0.0, min(1.0, float(s)))
        v = max(0.0, min(1.0, float(v)))

        if s == 0.0:
            r = g = b = int(round(v * 255))
            return (r, g, b)

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

        return (int(round(r * 255)), int(round(g * 255)), int(round(b * 255)))

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
            raise TypeError('index must be an integer')
        if index < 0:
            index = len(self._channels) + index
        if index < 0:
            raise IndexError('channel index out of range')
        if index >= len(self._channels):
            self._generate_channels(index - len(self._channels) + 1)
        return self._channels[index]

    def __len__(self):
        '''Return the number of generated channels.'''
        return len(self._channels)
