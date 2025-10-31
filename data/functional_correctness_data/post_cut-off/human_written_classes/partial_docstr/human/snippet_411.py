class ValidationResult:
    """ValidationResults store the output of a Requirement's validation. They can be used to return additional info from validation functions, which is useful for sampling/repairing."""

    def __init__(self, result: bool, *, reason: str | None=None, score: float | None=None):
        """The result of a requirement's validation.

        A ValidationResult's result field always contains a definitive pass/fail. The other fields can be used to communicate additional information about that result.

        Args:
            result: a boolean that is true if the requirement passed
            reason: a reason for the result
            score: if your validator gives you a score back, you can add this as metadata
        """
        self._result = result
        self._reason = reason
        self._score = score

    @property
    def reason(self) -> str | None:
        return self._reason

    @property
    def score(self) -> float | None:
        return self._score

    def as_bool(self) -> bool:
        """"""
        return self._result

    def __bool__(self) -> bool:
        return self.as_bool()