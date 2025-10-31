
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
        self.index = 0

    def _generate_channels(self, count):
        '''Generate the specified number of unique channel colors.'''
        for i in range(count):
            h = i / count
            s = 0.7
            v = 0.9
            rgb = self._hsv_to_rgb(h, s, v)
            label = f"Channel {i + 1}"
            self.channels.append({'label': label, 'color': rgb})

    @staticmethod
    def _hsv_to_rgb(h, s, v):
        '''Convert HSV color space to RGB color space.'''
        import colorsys
        return colorsys.hsv_to_rgb(h, s, v)

    def __iter__(self):
        '''Return the iterator object itself.'''
        self.index = 0
        return self

    def __next__(self):
        '''Return the next channel color.'''
        if self.index < len(self.channels):
            result = self.channels[self.index]
            self.index += 1
            return result
        else:
            # Generate a new channel color if we run out
            h = len(self.channels) / (len(self.channels) + 1)
            s = 0.7
            v = 0.9
            rgb = self._hsv_to_rgb(h, s, v)
            label = f"Channel {len(self.channels) + 1}"
            new_channel = {'label': label, 'color': rgb}
            self.channels.append(new_channel)
            return new_channel

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
            # Generate new channels up to the requested index
            self._generate_channels(index - len(self.channels) + 1)
            return self.channels[index]

    def __len__(self):
        '''Return the number of generated channels.'''
        return len(self.channels)
