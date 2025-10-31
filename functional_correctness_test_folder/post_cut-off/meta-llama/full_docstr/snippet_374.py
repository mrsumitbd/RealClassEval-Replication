
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
        self._generate_channels(num_channels)

    def _generate_channels(self, count):
        '''Generate the specified number of unique channel colors.'''
        for i in range(count):
            h = i / (count + 1)  # Avoid division by zero
            rgb = self._hsv_to_rgb(h, 1, 1)
            self._channels.append({
                'label': f'Channel {len(self._channels) + 1}',
                'color': tuple(int(channel * 255) for channel in rgb)
            })

    @staticmethod
    def _hsv_to_rgb(h, s, v):
        '''Convert HSV color space to RGB color space.'''
        return colorsys.hsv_to_rgb(h, s, v)

    def __iter__(self):
        '''Return the iterator object itself.'''
        return self

    def __next__(self):
        '''Return the next channel color.'''
        if self._index < len(self._channels):
            channel = self._channels[self._index]
            self._index += 1
            return channel
        else:
            self._generate_channels(1)
            return self.__next__()

    def get_channel(self, index):
        '''
        Get channel color by index.
        Args:
            index: Index of the channel to retrieve
        Returns:
            dict: Channel information with 'label' and 'color' keys
        '''
        if index < len(self._channels):
            return self._channels[index]
        else:
            self._generate_channels(index - len(self._channels) + 1)
            return self._channels[index]

    def __len__(self):
        '''Return the number of generated channels.'''
        return len(self._channels)
