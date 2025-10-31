class KEY_DERIVATION_STRING_DATA_MechanismBase:
    """Base class for mechanisms using derivation string data."""

    def __init__(self, data, mechType):
        """
        Initialize the mechanism with derivation string data and a mechanism type.

        Parameters
        ----------
        data : bytes, bytearray, or str
            The derivation string data. If a string is provided it will be
            encoded to UTF‑8 bytes when converting to native format.
        mechType : int
            An integer representing the mechanism type.
        """
        if not isinstance(data, (bytes, bytearray, str)):
            raise TypeError("data must be bytes, bytearray, or str")
        if not isinstance(mechType, int):
            raise TypeError("mechType must be an integer")

        self.data = data
        self.mechType = mechType

    def to_native(self):
        """
        Convert the mechanism to a native representation.

        Returns
        -------
        dict
            A dictionary containing the mechanism type and the data as bytes.
        """
        # Ensure data is bytes for the native representation
        native_data = (
            self.data
            if isinstance(self.data, (bytes, bytearray))
            else self.data.encode("utf-8")
        )
        return {"mechType": self.mechType, "data": native_data}

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(data={self.data!r}, "
            f"mechType={self.mechType!r})"
        )

    def __eq__(self, other):
        if not isinstance(other, KEY_DERIVATION_STRING_DATA_MechanismBase):
            return NotImplemented
        return self.data == other.data and self.mechType == other.mechType
