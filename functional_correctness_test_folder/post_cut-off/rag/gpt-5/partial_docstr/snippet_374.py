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
        if not isinstance(num_channels, int) or num_channels < 0:
            raise ValueError("num_channels must be a non-negative integer")
        self._channels = []
        self._yield_index = 0
        if num_channels:
            self._generate_channels(num_channels)

    def _generate_channels(self, count):
        '''Generate the specified number of unique channel colors.'''
        if count <= 0:
            return
        golden_ratio_conjugate = 0.61803398875
        start_len = len(self._channels)
        for i in range(count):
            idx = start_len + i
            # Evenly spread hues using golden ratio for good distinctness
            h = (idx * golden_ratio_conjugate) % 1.0

            # Cycle saturation/value in tiers to add variety for many channels
            tier = (idx // 24) % 3
            s_levels = (0.75, 0.60, 0.85)
            v_levels = (0.95, 0.80, 0.90)
            s = s_levels[tier]
            v = v_levels[tier]

            r, g, b = self._hsv_to_rgb(h, s, v)
            hex_color = '#{0:02X}{1:02X}{2:02X}'.format(r, g, b)

            self._channels.append({
                'label': f'Channel {idx + 1}',
                'color': hex_color
            })

    @staticmethod
    def _hsv_to_rgb(h, s, v):
        '''Convert HSV color space to RGB color space.'''
        # Clamp inputs
        h = 0.0 if h is None else max(0.0, min(1.0, float(h)))
        s = 0.0 if s is None else max(0.0, min(1.0, float(s)))
        v = 0.0 if v is None else max(0.0, min(1.0, float(v)))

        if s == 0.0:
            r = g = b = int(round(v * 255))
            return r, g, b

        h6 = h * 6.0
        i = int(h6)  # sector 0 to 5
        f = h6 - i
        p = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))
        i = i % 6

        if i == 0:
            r_, g_, b_ = v, t, p
        elif i == 1:
            r_, g_, b_ = q, v, p
        elif i == 2:
            r_, g_, b_ = p, v, t
        elif i == 3:
            r_, g_, b_ = p, q, v
        elif i == 4:
            r_, g_, b_ = t, p, v
        else:
            r_, g_, b_ = v, p, q

        r = int(round(r_ * 255))
        g = int(round(g_ * 255))
        b = int(round(b_ * 255))
        # Ensure bounds
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        return r, g, b

    def __iter__(self):
        '''Return the iterator object itself.'''
        self._yield_index = 0
        return self

    def __next__(self):
        '''Return the next channel color.'''
        if self._yield_index >= len(self._channels):
            self._generate_channels(1)
        item = self._channels[self._yield_index]
        self._yield_index += 1
        return item

    def get_channel(self, index):
        '''
        Get channel color by index.
        Args:
            index: Index of the channel to retrieve
        Returns:
            dict: Channel information with 'label' and 'color' keys
        '''
        if not isinstance(index, int) or index < 0:
            raise IndexError("index must be a non-negative integer")
        if index >= len(self._channels):
            self._generate_channels(index + 1 - len(self._channels))
        return self._channels[index]

    def __len__(self):
        '''Return the number of generated channels.'''
        return len(self._channels)
