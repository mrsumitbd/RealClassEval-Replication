class SpdxNone:
    """
    Represents the SPDX NONE value.
    """

    def __str__(self):
        return SPDX_NONE_STRING

    def __repr__(self):
        return SPDX_NONE_STRING

    def __eq__(self, other):
        return isinstance(other, SpdxNone)