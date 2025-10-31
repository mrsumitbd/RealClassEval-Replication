
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
        self.current_index = 0
        if num_channels > 0:
            self._generate_channels(num_channels)

    def _generate_channels(self, count):
        '''Generate the specified number of unique channel colors.'''
        for i in range(count):
            # Golden ratio for even distribution
            hue = (i * 0.618033988749895) % 1.0
            # Alternate between two saturation levels
            saturation = 0.7 + (i % 2) * 0.2
            value = 0.8 + (i % 3) * 0.1  # Alternate between three value levels
            rgb = self._hsv_to_rgb(hue, saturation, value)
            self.channels.append({
                'label': f'Channel {i+1}',
                'color': rgb
            })

    @staticmethod
    def _hsv_to_rgb(h, s, v):
        '''Convert HSV color space to RGB color space.'''
        if s == 0.0:
            return (v, v, v)
        i = int(h * 6.0)
        f = (h * 6.0) - i
        p = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))
        i = i % 6
        if i == 0:
            return (v, t, p)
        if i == 1:
            return (q, v, p)
        if i == 2:
            return (p, v, t)
        if i == 3:
            return (p, q, v)
        if i == 4:
            return (t, p, v)
        if i == 5:
            return (v, p, q)

    def __iter__(self):
        '''Return the iterator object itself.'''
        return self

    def __next__(self):
        '''Return the next channel color.'''
        if self.current_index >= len(self.channels):
            self._generate_channels(1)
        channel = self.channels[self.current_index]
        self.current_index += 1
        return channel

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
