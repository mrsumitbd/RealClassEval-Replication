
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
        self._channels = []
        self._index = 0
        if num_channels > 0:
            self._generate_channels(num_channels)

    def _generate_channels(self, count):
        '''Generate the specified number of unique channel colors.'''
        start = len(self._channels)
        for i in range(start, start + count):
            # Distribute hues evenly around the color wheel
            # Golden ratio for good distribution
            h = (i * 0.618033988749895) % 1.0
            # Alternate saturation a bit
            s = 0.65 + 0.25 * ((i % 2) * 2 - 1) * 0.2
            v = 0.85 if i % 3 != 0 else 0.65  # Alternate value for some variety
            rgb = self._hsv_to_rgb(h, s, v)
            color = '#{:02x}{:02x}{:02x}'.format(*rgb)
            label = f'Channel {i+1}'
            self._channels.append({'label': label, 'color': color})

    @staticmethod
    def _hsv_to_rgb(h, s, v):
        '''Convert HSV color space to RGB color space.'''
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
        self._index = 0
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
