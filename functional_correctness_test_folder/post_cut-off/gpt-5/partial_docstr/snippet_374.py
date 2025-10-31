class ChannelIterator:

    def __init__(self, num_channels=0):
        '''
        Initialize the channel iterator.
        Args:
            num_channels: Initial number of channels to pre-generate
        '''
        self._channels = []
        self._iter_index = 0
        self._hue_index = 0
        if num_channels > 0:
            self._generate_channels(num_channels)

    def _generate_channels(self, count):
        '''Generate the specified number of unique channel colors.'''
        # Use golden ratio conjugate to distribute hues uniformly
        phi_conj = 0.618033988749895
        for _ in range(count):
            h = (self._hue_index * phi_conj) % 1.0
            s = 0.6
            v = 0.95
            r, g, b = self._hsv_to_rgb(h, s, v)
            label = f"Channel {len(self._channels) + 1}"
            self._channels.append({
                'label': label,
                'color': (r, g, b)
            })
            self._hue_index += 1

    @staticmethod
    def _hsv_to_rgb(h, s, v):
        '''Convert HSV color space to RGB color space.'''
        if s == 0.0:
            r = g = b = int(round(v * 255))
            return r, g, b

        h = (h % 1.0) * 6.0
        i = int(h)
        f = h - i
        p = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))

        if i == 0:
            r_f, g_f, b_f = v, t, p
        elif i == 1:
            r_f, g_f, b_f = q, v, p
        elif i == 2:
            r_f, g_f, b_f = p, v, t
        elif i == 3:
            r_f, g_f, b_f = p, q, v
        elif i == 4:
            r_f, g_f, b_f = t, p, v
        else:
            r_f, g_f, b_f = v, p, q

        r = int(round(r_f * 255))
        g = int(round(g_f * 255))
        b = int(round(b_f * 255))
        return r, g, b

    def __iter__(self):
        '''Return the iterator object itself.'''
        return self

    def __next__(self):
        '''Return the next channel color.'''
        if self._iter_index >= len(self._channels):
            self._generate_channels(1)
        item = self._channels[self._iter_index]
        self._iter_index += 1
        return item

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
        if index >= len(self._channels):
            self._generate_channels(index - len(self._channels) + 1)
        return self._channels[index]

    def __len__(self):
        '''Return the number of generated channels.'''
        return len(self._channels)
