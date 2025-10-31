
class ChannelIterator:

    def __init__(self, num_channels=0):
        '''
        Initialize the channel iterator.
        Args:
            num_channels: Initial number of channels to pre-generate
        '''
        self.channels = self._generate_channels(num_channels)
        self.index = 0

    def _generate_channels(self, count):
        '''Generate the specified number of unique channel colors.'''
        channels = []
        for i in range(count):
            h = i / count
            rgb = self._hsv_to_rgb(h, 1, 1)
            channels.append({'label': f'Channel {i+1}', 'color': rgb})
        return channels

    @staticmethod
    def _hsv_to_rgb(h, s, v):
        '''Convert HSV color space to RGB color space.'''
        h_i = int(h * 6)
        f = h * 6 - h_i
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)

        if h_i == 0:
            r, g, b = v, t, p
        elif h_i == 1:
            r, g, b = q, v, p
        elif h_i == 2:
            r, g, b = p, v, t
        elif h_i == 3:
            r, g, b = p, q, v
        elif h_i == 4:
            r, g, b = t, p, v
        elif h_i == 5:
            r, g, b = v, p, q

        return (int(r * 255), int(g * 255), int(b * 255))

    def __iter__(self):
        '''Return the iterator object itself.'''
        return self

    def __next__(self):
        '''Return the next channel color.'''
        if self.index < len(self.channels):
            channel = self.channels[self.index]
            self.index += 1
            return channel
        else:
            raise StopIteration

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
            count = index - len(self.channels) + 1
            new_channels = self._generate_channels(count)
            self.channels.extend(new_channels)
            return new_channels[-1]

    def __len__(self):
        '''Return the number of generated channels.'''
        return len(self.channels)


# Example usage:
if __name__ == "__main__":
    channel_iterator = ChannelIterator(5)
    for _ in range(10):
        print(next(channel_iterator))

    print(channel_iterator.get_channel(3))
    print(len(channel_iterator))
