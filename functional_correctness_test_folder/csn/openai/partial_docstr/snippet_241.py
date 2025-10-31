
class Issue:
    """Represents an issue with optional external data and payload generation."""

    _VALID_PREFIXES = ("pb", "ab", "si", "ti")
    _VALID_EXACT = ("nd001",)

    def __init__(self, issue_type, comment=None, auto_analyzed=False, ignore_analyzer=True):
        """
        Initialize instance attributes.

        :param issue_type: Issue type locator. Allowable values: "pb***",
                           "ab***", "si***", "ti***", "nd001". Where *** is locator id.
        :param comment: Issue comments
        :param auto_analyzed: Indicator that the issue has been marked with
                              the RP auto analyzer
        :param ignore_analyzer: Flag that forces RP analyzer to ignore this
                                issue
        """
        if not isinstance(issue_type, str):
            raise TypeError("issue_type must be a string")

        # Validate issue_type
        if issue_type in self._VALID_EXACT:
            pass
        else:
            prefix = issue_type[:2]
            if prefix not in self._VALID_PREFIXES:
                raise ValueError(
                    f"Invalid issue_type prefix '{prefix}'. "
                    f"Expected one of {self._VALID_PREFIXES} or 'nd001'."
                )
            if len(issue_type) <= 2:
                raise ValueError(
                    f"issue_type '{issue_type}' must contain an id after the prefix."
                )

        self.issue_type = issue_type
        self.comment = comment
        self.auto_analyzed = bool(auto_analyzed)
        self.ignore_analyzer = bool(ignore_analyzer)
        self._external_issue = None

    def external_issue_add(self, issue):
        """
        Attach an external issue representation.

        :param issue: Any object representing an external issue.
        """
        self._external_issue = issue

    @property
    def payload(self):
        """
        Form the correct dictionary for the issue.

        :return: dict containing issue data ready for serialization.
        """
        data = {
            "issue_type": self.issue_type,
            "auto_analyzed": self.auto_analyzed,
            "ignore_analyzer": self.ignore_analyzer,
        }
        if self.comment is not None:
            data["comment"] = self.comment
        if self._external_issue is not None:
            data["external_issue"] = self._external_issue
        return data
