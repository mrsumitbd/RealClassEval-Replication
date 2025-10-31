
import random
import colorsys


class ChannelIterator:
    def __init__(self, num_channels=0):
        """
        Initialize the channel iterator.
        Args:
            num_channels: Initial number of channels to pre-generate
        """
        self._channels = []
        self._index = 0
        if num_channels > 0:
            self._generate_channels(num_channels)

    def _generate_channels(self, count):
        """Generate the specified number of unique channel colors."""
        generated = 0
        while generated < count:
            # Random hue, fixed saturation and value for bright colors
            h = random.random()
            s = 0.5 + 0.5 * random.random()  # 0.5 to 1.0
            v = 0.8 + 0.2 * random.random()  # 0.8 to 1.0
            r, g, b = self._hsv_to_rgb(h, s, v)
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            # Ensure uniqueness
            if not any(ch["color"] == hex_color for ch in self._channels):
                label = f"Channel {len(self._channels)}"
                self._channels.append({"label": label, "color": hex_color})
                generated += 1

    @staticmethod
    def _hsv_to_rgb(h, s, v):
        """Convert HSV color space to RGB color space."""
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return int(r * 255), int(g * 255), int(b * 255)

    def __iter__(self):
        """Return the iterator object itself."""
        return self

    def __next__(self):
        """Return the next channel color."""
        if self._index >= len(self._channels):
            raise StopIteration
        channel = self._channels[self._index]
        self._index += 1
        return channel

    def get_channel(self, index):
        """
        Get channel color by index.
        Args:
            index: Index of the channel to retrieve
        Returns:
            dict: Channel information with 'label' and 'color' keys
        """
        if index < 0 or index >= len(self._channels):
            raise IndexError("Channel index out of range")
        return self._channels[index]

    def __len__(self):
        """Return the number of generated channels."""
        return len(self._channels)
