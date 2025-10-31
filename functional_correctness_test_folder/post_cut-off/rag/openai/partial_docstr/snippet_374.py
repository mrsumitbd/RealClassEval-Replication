
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
        self.channels = []          # list of dicts with 'label' and 'color'
        self._next_index = 0        # index used by __next__
        if num_channels > 0:
            self._generate_channels(num_channels)

    def _generate_channels(self, count):
        '''Generate the specified number of unique channel colors.'''
        # Use the golden angle to space hues evenly
        GOLDEN_ANGLE = 137.508  # degrees
        start = len(self.channels)
        for i in range(count):
            hue = (start + i) * GOLDEN_ANGLE % 360
            sat = 0.5
            val = 0.95
            r, g, b = self._hsv_to_rgb(hue / 360.0, sat, val)
            hex_color = f'#{r:02X}{g:02X}{b:02X}'
            label = f'Channel {start + i}'
            self.channels.append({'label': label, 'color': hex_color})

    @staticmethod
    def _hsv_to_rgb(h, s, v):
        '''Convert HSV color space to RGB color space.'''
        # h in [0,1], s in [0,1], v in [0,1]
        if s == 0.0:
            r = g = b = int(v * 255)
            return r, g, b
        i = int(h * 6.0)  # sector 0 to 5
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
        return int(r * 255), int(g * 255), int(b * 255)

    def __iter__(self):
        '''Return the iterator object itself.'''
        return self

    def __next__(self):
        '''Return the next channel color.'''
        if self._next_index >= len(self.channels):
            # generate a batch of new channels when needed
            self._generate_channels(10)
        channel = self.channels[self._next_index]
        self._next_index += 1
        return channel

    def get_channel(self, index):
        '''
        Get channel color by index.
        Args:
            index: Index of the channel to retrieve
        Returns:
            dict: Channel information with 'label' and 'color' keys
        '''
        if index < 0:
            raise IndexError('Channel index must be non‑negative')
        while index >= len(self.channels):
            self._generate_channels(10)
        return self.channels[index]

    def __len__(self):
        '''Return the number of generated channels.'''
        return len(self.channels)
