
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
        self.channels = []
        self.index = 0
        if num_channels > 0:
            self._generate_channels(num_channels)

    def _generate_channels(self, count):
        '''Generate the specified number of unique channel colors.'''
        start = len(self.channels)
        for i in range(start, start + count):
            # Use golden ratio to distribute hues
            golden_ratio_conjugate = 0.618033988749895
            h = (i * golden_ratio_conjugate) % 1.0
            s = 0.65
            v = 0.95
            rgb = self._hsv_to_rgb(h, s, v)
            color = '#{:02x}{:02x}{:02x}'.format(*rgb)
            label = f'Channel {i+1}'
            self.channels.append({'label': label, 'color': color})

    @staticmethod
    def _hsv_to_rgb(h, s, v):
        '''Convert HSV color space to RGB color space.'''
        import math
        h = float(h)
        s = float(s)
        v = float(v)
        if s == 0.0:
            r = g = b = int(v * 255)
            return (r, g, b)
        i = int(h * 6.0)
        f = (h * 6.0) - i
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
        elif i == 5:
            r, g, b = v, p, q
        return (int(r * 255), int(g * 255), int(b * 255))

    def __iter__(self):
        '''Return the iterator object itself.'''
        self.index = 0
        return self

    def __next__(self):
        '''Return the next channel color.'''
        if self.index >= len(self.channels):
            self._generate_channels(1)
        result = self.channels[self.index]
        self.index += 1
        return result

    def get_channel(self, index):
        '''
        Get channel color by index.
        Args:
            index: Index of the channel to retrieve
        Returns:
            dict: Channel information with 'label' and 'color' keys
        '''
        if index >= len(self.channels):
            self._generate_channels(index - len(self.channels) + 1)
        return self.channels[index]

    def __len__(self):
        '''Return the number of generated channels.'''
        return len(self.channels)
