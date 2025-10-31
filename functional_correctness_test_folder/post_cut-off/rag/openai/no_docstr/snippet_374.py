
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
        self._index = 0             # iterator position
        if num_channels > 0:
            self._generate_channels(num_channels)

    def _generate_channels(self, count):
        '''Generate the specified number of unique channel colors.'''
        # Determine how many new channels to add
        start = len(self.channels)
        end = start + count
        # Use evenly spaced hues
        for i in range(start, end):
            # Hue in [0,1)
            h = (i / max(1, end))  # avoid division by zero
            s = 0.5
            v = 0.95
            r, g, b = self._hsv_to_rgb(h, s, v)
            hex_color = f'#{r:02x}{g:02x}{b:02x}'
            label = f'Channel {i}'
            self.channels.append({'label': label, 'color': hex_color})

    @staticmethod
    def _hsv_to_rgb(h, s, v):
        '''Convert HSV color space to RGB color space.'''
        # h in [0,1), s in [0,1], v in [0,1]
        i = int(h * 6)  # sector 0 to 5
        f = h * 6 - i
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)
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
        else:  # i == 5
            r, g, b = v, p, q
        return int(r * 255), int(g * 255), int(b * 255)

    def __iter__(self):
        '''Return the iterator object itself.'''
        return self

    def __next__(self):
        '''Return the next channel color.'''
        if self._index >= len(self.channels):
            # generate one more channel
            self._generate_channels(1)
        channel = self.channels[self._index]
        self._index += 1
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
        # generate until we have enough
        while index >= len(self.channels):
            self._generate_channels(1)
        return self.channels[index]

    def __len__(self):
        '''Return the number of generated channels.'''
        return len(self.channels)
