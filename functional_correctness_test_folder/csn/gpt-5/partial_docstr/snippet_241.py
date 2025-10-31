class Issue:

    def __init__(self, issue_type, comment=None, auto_analyzed=False, ignore_analyzer=True):
        '''Initialize instance attributes.
        :param issue_type:      Issue type locator. Allowable values: "pb***",
                                "ab***", "si***", "ti***", "nd001". Where ***
                                is locator id.
        :param comment:         Issue comments
        :param auto_analyzed:   Indicator that the issue has been marked with
                                the RP auto analyzer
        :param ignore_analyzer: Flag that forces RP analyzer to ignore this
                                issue
        '''
        import re

        if not isinstance(issue_type, str):
            raise TypeError("issue_type must be a string")
        if not re.match(r'^(pb|ab|si|ti)\d{3}$|^nd001$', issue_type):
            raise ValueError(
                'issue_type must match "pb***", "ab***", "si***", "ti***" with 3 digits, or be "nd001"')

        self.issue_type = issue_type
        self.comment = None if comment is None else str(comment)
        self.auto_analyzed = bool(auto_analyzed)
        self.ignore_analyzer = bool(ignore_analyzer)
        self._external_system_issues = []

    def external_issue_add(self, issue):
        if issue is None:
            raise ValueError("issue cannot be None")
        if not isinstance(issue, dict):
            raise TypeError("issue must be a dict")
        # Shallow copy to avoid external mutation
        self._external_system_issues.append(dict(issue))
        return self

    @property
    def payload(self):
        '''Form the correct dictionary for the issue.'''
        data = {
            "issueType": self.issue_type,
            "autoAnalyzed": self.auto_analyzed,
            "ignoreAnalyzer": self.ignore_analyzer,
        }
        if self.comment is not None:
            data["comment"] = self.comment
        if self._external_system_issues:
            data["externalSystemIssues"] = list(self._external_system_issues)
        return data
