
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
        self._channels = []
        self._index = 0
        if num_channels > 0:
            self._generate_channels(num_channels)

    def _generate_channels(self, count):
        '''Generate the specified number of unique channel colors.'''
        for i in range(len(self._channels), len(self._channels) + count):
            # Golden ratio for distinct hues
            hue = (i * 0.618033988749895) % 1.0
            rgb = self._hsv_to_rgb(hue, 0.8, 0.8)
            self._channels.append({
                'label': f'Channel {i + 1}',
                'color': rgb
            })

    @staticmethod
    def _hsv_to_rgb(h, s, v):
        '''Convert HSV color space to RGB color space.'''
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return (int(r * 255), int(g * 255), int(b * 255))

    def __iter__(self):
        '''Return the iterator object itself.'''
        self._index = 0
        return self

    def __next__(self):
        '''Return the next channel color.'''
        if self._index >= len(self._channels):
            self._generate_channels(1)
        channel = self._channels[self._index]
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
        if index >= len(self._channels):
            self._generate_channels(index - len(self._channels) + 1)
        return self._channels[index]

    def __len__(self):
        '''Return the number of generated channels.'''
        return len(self._channels)
