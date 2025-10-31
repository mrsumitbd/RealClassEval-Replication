
class CkClass:
    """
    Base class for CK_* classes
    """

    # Mapping of flag bit values to their textual representation.
    # Subclasses can override or extend this dictionary.
    FLAG_MAP = {}

    def flags2text(self):
        """
        Parse the `self.flags` field and create a list of `CKF_*` strings
        corresponding to bits set in flags.

        :return: a list of strings
        :rtype: list
        """
        flags = getattr(self, "flags", None)
        if not isinstance(flags, int):
            return []

        result = []
        for bit, name in self.FLAG_MAP.items():
            if flags & bit:
                result.append(name)
        return result

    def state2text(self):
        """
        Dummy method. Will be overridden if necessary.
        """
        return None

    def to_dict(self):
        """
        Convert the fields of the object into a dictionary.
        """
        # Use a shallow copy to avoid accidental modifications.
        return dict(vars(self))

    def __str__(self):
        """
        Text representation of the object.
        """
        return f"{self.__class__.__name__}({self.to_dict()})"
