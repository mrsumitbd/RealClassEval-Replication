class Issue:
    """This class represents an issue that can be attached to test result."""

    def __init__(self, issue_type, comment=None, auto_analyzed=False, ignore_analyzer=True):
        """Initialize instance attributes.

        :param issue_type:      Issue type locator. Allowable values: "pb***",
                                "ab***", "si***", "ti***", "nd001". Where ***
                                is locator id.
        :param comment:         Issue comments
        :param auto_analyzed:   Indicator that the issue has been marked with
                                the RP auto analyzer
        :param ignore_analyzer: Flag that forces RP analyzer to ignore this
                                issue
        """
        self._external_issues = []
        self.auto_analyzed = auto_analyzed
        self.comment = comment
        self.ignore_analyzer = ignore_analyzer
        self.issue_type = issue_type

    def external_issue_add(self, issue):
        """Add external system issue to the issue."""
        self._external_issues.append(issue.payload)

    @property
    def payload(self):
        """Form the correct dictionary for the issue."""
        return {'autoAnalyzed': self.auto_analyzed, 'comment': self.comment, 'externalSystemIssues': self._external_issues, 'ignoreAnalyzer': self.ignore_analyzer, 'issueType': self.issue_type}