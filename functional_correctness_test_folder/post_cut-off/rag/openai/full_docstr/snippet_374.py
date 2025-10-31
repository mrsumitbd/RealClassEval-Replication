
import colorsys
import math


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
        self._index = 0
        if num_channels > 0:
            self._generate_channels(num_channels)

    def _generate_channels(self, count):
        '''Generate the specified number of unique channel colors.'''
        # Use the golden ratio conjugate to space hues evenly
        golden_ratio_conjugate = 0.618033988749895
        hue = 0.0
        for _ in range(count):
            # Increment hue by golden ratio conjugate
            hue = (hue + golden_ratio_conjugate) % 1.0
            # Fixed saturation and value for bright, distinct colors
            s = 0.5
            v = 0.95
            r, g, b = self._hsv_to_rgb(hue, s, v)
            hex_color = f'#{r:02x}{g:02x}{b:02x}'
            label = f'Channel {len(self.channels)}'
            self.channels.append({'label': label, 'color': hex_color})

    @staticmethod
    def _hsv_to_rgb(h, s, v):
        '''Convert HSV color space to RGB color space.'''
        # colorsys uses h,s,v in [0,1]
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        # Convert to 0-255 integer values
        return int(r * 255), int(g * 255), int(b * 255)

    def __iter__(self):
        '''Return the iterator object itself.'''
        return self

    def __next__(self):
        '''Return the next channel color.'''
        if self._index >= len(self.channels):
            raise StopIteration
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
        # Generate more channels if needed
        while index >= len(self.channels):
            self._generate_channels(1)
        return self.channels[index]

    def __len__(self):
        '''Return the number of generated channels.'''
        return len(self.channels)
