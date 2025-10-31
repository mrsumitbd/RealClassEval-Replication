
class WordArray:
    """
    A simple container that stores a sequence of 32‑bit words derived from a
    bytes‑like object.  Words are stored in big‑endian order.
    """

    def __init__(self, bytes_obj):
        """
        Convert a bytes‑like object into a list of 32‑bit words.

        Parameters
        ----------
        bytes_obj : bytes or bytearray
            The source data.  If the length is not a multiple of 4, the last
            word is padded with zero bytes on the right.
        """
        if not isinstance(bytes_obj, (bytes, bytearray)):
            raise TypeError("bytes_obj must be bytes or bytearray")

        self._words = []
        # Process each 4‑byte block
        for i in range(0, len(bytes_obj), 4):
            block = bytes_obj[i:i + 4]
            # Pad the block to 4 bytes if necessary
            if len(block) < 4:
                block = block + b'\x00' * (4 - len(block))
            # Convert to a 32‑bit integer (big‑endian)
            word = (
                (block[0] << 24)
                | (block[1] << 16)
                | (block[2] << 8)
                | block[3]
            )
            self._words.append(word)

    def __len__(self):
        """Return the number of 32‑bit words."""
        return len(self._words)

    def __getitem__(self, key):
        """
        Retrieve a word or a slice of words.

        Parameters
        ----------
        key : int or slice
            If an integer, returns the word at that index (supports negative
            indices).  If a slice, returns a new WordArray containing the
            sliced words.

        Returns
        -------
        int or WordArray
            The requested word or a new WordArray.
        """
        if isinstance(key, slice):
            # Return a new WordArray with the sliced words
            sliced_words = self._words[key]
            # Construct a new WordArray from the sliced words
            new_obj = WordArray(b'')
            new_obj._words = sliced_words
            return new_obj
        elif isinstance(key, int):
            return self._words[key]
        else:
            raise TypeError("Index must be an int or slice")

    def __repr__(self):
        return f"WordArray({self._words!r})"
