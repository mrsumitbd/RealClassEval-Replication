
import colorsys


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
        self._generate_channels(num_channels)

    def _generate_channels(self, count):
        '''Generate the specified number of unique channel colors.'''
        for _ in range(count):
            # Spread colors across the hue spectrum
            h = len(self.channels) / 10.0
            s = 0.8  # Moderate to high saturation for distinct colors
            v = 0.9  # Bright colors
            r, g, b = self._hsv_to_rgb(h, s, v)
            self.channels.append(
                {'label': f'Channel {len(self.channels)}', 'color': (r, g, b)})

    @staticmethod
    def _hsv_to_rgb(h, s, v):
        '''Convert HSV color space to RGB color space.'''
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return int(r * 255), int(g * 255), int(b * 255)

    def __iter__(self):
        '''Return the iterator object itself.'''
        return self

    def __next__(self):
        '''Return the next channel color.'''
        if self.index >= len(self.channels):
            self._generate_channels(10)  # Generate more channels if needed
        channel = self.channels[self.index]
        self.index += 1
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
