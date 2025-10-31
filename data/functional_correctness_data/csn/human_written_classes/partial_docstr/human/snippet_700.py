class SpdxNoAssertion:
    """
    Represents the SPDX NOASSERTION value.
    """

    def __str__(self):
        return SPDX_NO_ASSERTION_STRING

    def __repr__(self):
        return SPDX_NO_ASSERTION_STRING

    def __eq__(self, other):
        return isinstance(other, SpdxNoAssertion)