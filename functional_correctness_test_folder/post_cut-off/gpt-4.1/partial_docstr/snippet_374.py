
class ChannelIterator:

    def __init__(self, num_channels=0):
        '''
        Initialize the channel iterator.
        Args:
            num_channels: Initial number of channels to pre-generate
        '''
        self._channels = []
        self._index = 0
        if num_channels > 0:
            self._generate_channels(num_channels)

    def _generate_channels(self, count):
        '''Generate the specified number of unique channel colors.'''
        start = len(self._channels)
        for i in range(start, start + count):
            # Golden ratio for good color distribution
            h = (i * 0.618033988749895) % 1.0
            s = 0.5 + 0.5 * ((i % 2) * 0.5)   # Alternate saturation
            v = 0.95 if (i % 3) != 0 else 0.8  # Alternate value
            rgb = self._hsv_to_rgb(h, s, v)
            color = '#{:02X}{:02X}{:02X}'.format(*rgb)
            label = f'Channel {i+1}'
            self._channels.append({'label': label, 'color': color})

    @staticmethod
    def _hsv_to_rgb(h, s, v):
        '''Convert HSV color space to RGB color space.'''
        import colorsys
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return (int(r * 255), int(g * 255), int(b * 255))

    def __iter__(self):
        '''Return the iterator object itself.'''
        return self

    def __next__(self):
        '''Return the next channel color.'''
        if self._index >= len(self._channels):
            self._generate_channels(1)
        result = self._channels[self._index]
        self._index += 1
        return result

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
            self._generate_channels(index - len(self._channels) + 1)
        return self._channels[index]

    def __len__(self):
        '''Return the number of generated channels.'''
        return len(self._channels)
