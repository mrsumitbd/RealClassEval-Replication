
import colorsys


class ChannelIterator:

    def __init__(self, num_channels=0):
        '''
        Initialize the channel iterator.
        Args:
            num_channels: Initial number of channels to pre-generate
        '''
        self._channels = []
        if num_channels > 0:
            self._generate_channels(num_channels)

    def _generate_channels(self, count):
        '''Generate the specified number of unique channel colors.'''
        start = len(self._channels)
        for i in range(start, start + count):
            hue = (i * 360.0 / max(1, start + count)) % 360.0
            r, g, b = self._hsv_to_rgb(hue / 360.0, 1.0, 1.0)
            color = (int(r * 255), int(g * 255), int(b * 255))
            self._channels.append({
                'label': f'channel_{i}',
                'color': color
            })

    @staticmethod
    def _hsv_to_rgb(h, s, v):
        '''Convert HSV color space to RGB color space.'''
        return colorsys.hsv_to_rgb(h, s, v)

    def __iter__(self):
        '''Return the iterator object itself.'''
        self._current = 0
        return self

    def __next__(self):
        '''Return the next channel color.'''
        if self._current >= len(self._channels):
            self._generate_channels(1)
        channel = self._channels[self._current]
        self._current += 1
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
            raise IndexError("Index cannot be negative")
        while index >= len(self._channels):
            self._generate_channels(index - len(self._channels) + 1)
        return self._channels[index]

    def __len__(self):
        '''Return the number of generated channels.'''
        return len(self._channels)
