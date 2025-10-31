class KEY_DERIVATION_STRING_DATA_MechanismBase:
    """
    Base class for key derivation mechanisms that use a string (bytes) as data.
    """

    def __init__(self, data, mechType):
        """
        Initialize the mechanism with the given data and mechanism type.

        Parameters
        ----------
        data : bytes or bytearray or str
            The data to be used for the key derivation. If a string is provided,
            it will be encoded using UTF-8.
        mechType : int
            The numeric identifier of the mechanism type.
        """
        if not isinstance(mechType, int):
            raise TypeError(
                f"mechType must be an integer, got {type(mechType).__name__}")

        if isinstance(data, str):
            data = data.encode("utf-8")

        if not isinstance(data, (bytes, bytearray)):
            raise TypeError(
                f"data must be bytes, bytearray, or str, got {type(data).__name__}")

        self.data = data
        self.mechType = mechType

    def to_native(self):
        """
        Convert the mechanism to a native representation suitable for the
        underlying cryptographic library.

        Returns
        -------
        tuple
            A tuple of the form (mechType, data) where mechType is an integer
            and data is a bytes object.
        """
        return (self.mechType, self.data)
