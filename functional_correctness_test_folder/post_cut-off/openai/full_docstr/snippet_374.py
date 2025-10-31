
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
        self._channels = []
        self._next_index = 0
        if num_channels > 0:
            self._generate_channels(num_channels)

    def _generate_channels(self, count):
        '''Generate the specified number of unique channel colors.'''
        # Use the golden angle to space hues evenly
        golden_angle = 137.50776405003785  # degrees
        start_hue = 0.0
        # If we already have channels, start from the last hue
        if self._channels:
            last_hue = self._channels[-1]['hue']
            start_hue = (last_hue + golden_angle) % 360

        for i in range(count):
            hue = (start_hue + i * golden_angle) % 360
            rgb = self._hsv_to_rgb(hue / 360.0, 0.5, 0.95)
            hex_color = '#{:02X}{:02X}{:02X}'.format(*rgb)
            label = f'Channel {len(self._channels) + 1}'
            self._channels.append(
                {'label': label, 'color': hex_color, 'hue': hue})

    @staticmethod
    def _hsv_to_rgb(h, s, v):
        '''Convert HSV color space to RGB color space.'''
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return (int(r * 255), int(g * 255), int(b * 255))

    def __iter__(self):
        '''Return the iterator object itself.'''
        return self

    def __next__(self):
        '''Return the next channel color.'''
        if self._next_index >= len(self._channels):
            # Generate a batch of new channels when needed
            self._generate_channels(10)
        channel = self._channels[self._next_index]
        self._next_index += 1
        # Return only label and color, not internal hue
        return {'label': channel['label'], 'color': channel['color']}

    def get_channel(self, index):
        '''
        Get channel color by index.
        Args:
            index: Index of the channel to retrieve
        Returns:
            dict: Channel information with 'label' and 'color' keys
        '''
        if index < 0:
            raise IndexError("Index must be non‑negative")
        # Generate channels until we have enough
        while index >= len(self._channels):
            self._generate_channels(10)
        channel = self._channels[index]
        return {'label': channel['label'], 'color': channel['color']}

    def __len__(self):
        '''Return the number of generated channels.'''
        return len(self._channels)
