
class Issue:
    """
    Represents an issue with optional external issues attached.
    """

    def __init__(self, issue_type, comment=None, auto_analyzed=False, ignore_analyzer=True):
        """
        Initialize an Issue instance.

        Parameters
        ----------
        issue_type : str
            The type/category of the issue.
        comment : str, optional
            A textual comment describing the issue.
        auto_analyzed : bool, optional
            Flag indicating whether the issue was automatically analyzed.
        ignore_analyzer : bool, optional
            Flag indicating whether the analyzer should ignore this issue.
        """
        self.issue_type = issue_type
        self.comment = comment
        self.auto_analyzed = bool(auto_analyzed)
        self.ignore_analyzer = bool(ignore_analyzer)
        self._external_issues = []

    def external_issue_add(self, issue):
        """
        Add an external issue to this issue.

        Parameters
        ----------
        issue : Issue or dict
            The external issue to add. If a dict is provided, it is stored as-is.
        """
        if isinstance(issue, Issue):
            self._external_issues.append(issue)
        elif isinstance(issue, dict):
            self._external_issues.append(issue)
        else:
            raise TypeError(
                "external_issue_add expects an Issue instance or a dict")

    @property
    def payload(self):
        """
        Return a dictionary representation of the issue, including any external issues.

        Returns
        -------
        dict
            A dictionary containing the issue data.
        """
        payload = {
            "issue_type": self.issue_type,
            "comment": self.comment,
            "auto_analyzed": self.auto_analyzed,
            "ignore_analyzer": self.ignore_analyzer,
            "external_issues": [],
        }

        for ext in self._external_issues:
            if isinstance(ext, Issue):
                payload["external_issues"].append(ext.payload)
            else:
                payload["external_issues"].append(ext)

        return payload
