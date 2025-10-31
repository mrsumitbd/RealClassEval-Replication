class Issue:

    def __init__(self, issue_type, comment=None, auto_analyzed=False, ignore_analyzer=True):
        if not isinstance(issue_type, str) or not issue_type:
            raise ValueError("issue_type must be a non-empty string")
        self.issue_type = issue_type
        self.comment = comment
        self.auto_analyzed = bool(auto_analyzed)
        self.ignore_analyzer = bool(ignore_analyzer)
        self._external_issues = []

    def external_issue_add(self, issue):
        if not isinstance(issue, dict):
            raise TypeError("issue must be a dict")
        if not issue:
            raise ValueError("issue cannot be empty")
        self._external_issues.append(issue)

    @property
    def payload(self):
        data = {
            "issueType": self.issue_type,
            "autoAnalyzed": self.auto_analyzed,
            "ignoreAnalyzer": self.ignore_analyzer,
        }
        if self.comment is not None:
            data["comment"] = self.comment
        if self._external_issues:
            data["externalSystemIssues"] = list(self._external_issues)
        return data
