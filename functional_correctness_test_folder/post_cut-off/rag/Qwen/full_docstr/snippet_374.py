
import colorsys
import random


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
        self._generate_channels(num_channels)

    def _generate_channels(self, count):
        '''Generate the specified number of unique channel colors.'''
        for _ in range(count):
            h = random.random()
            # Ensure saturation is high enough for visibility
            s = random.uniform(0.5, 1.0)
            # Ensure value is high enough for visibility
            v = random.uniform(0.5, 1.0)
            rgb = self._hsv_to_rgb(h, s, v)
            label = f"Channel {len(self.channels)}"
            self.channels.append({'label': label, 'color': rgb})

    @staticmethod
    def _hsv_to_rgb(h, s, v):
        '''Convert HSV color space to RGB color space.'''
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return int(r * 255), int(g * 255), int(b * 255)

    def __iter__(self):
        '''Return the iterator object itself.'''
        self._index = 0
        return self

    def __next__(self):
        '''Return the next channel color.'''
        if self._index < len(self.channels):
            result = self.channels[self._index]
            self._index += 1
            return result
        else:
            # Generate a new channel if we've run out
            self._generate_channels(1)
            result = self.channels[self._index]
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
        if index < len(self.channels):
            return self.channels[index]
        else:
            # Generate more channels if the requested index is out of range
            self._generate_channels(index - len(self.channels) + 1)
            return self.channels[index]

    def __len__(self):
        '''Return the number of generated channels.'''
        return len(self.channels)
