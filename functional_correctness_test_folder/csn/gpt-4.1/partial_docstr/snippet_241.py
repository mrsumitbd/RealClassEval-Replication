
class Issue:

    def __init__(self, issue_type, comment=None, auto_analyzed=False, ignore_analyzer=True):
        '''
        Initialize instance attributes.
        :param issue_type:      Issue type locator. Allowable values: "pb***",
                                "ab***", "si***", "ti***", "nd001". Where ***
                                is locator id.
        :param comment:         Issue comments
        :param auto_analyzed:   Indicator that the issue has been marked with
                                the RP auto analyzer
        :param ignore_analyzer: Flag that forces RP analyzer to ignore this
                                issue
        '''
        self.issue_type = issue_type
        self.comment = comment
        self.auto_analyzed = auto_analyzed
        self.ignore_analyzer = ignore_analyzer
        self.external_issues = []

    def external_issue_add(self, issue):
        self.external_issues.append(issue)

    @property
    def payload(self):
        data = {
            "issue_type": self.issue_type,
            "auto_analyzed": self.auto_analyzed,
            "ignore_analyzer": self.ignore_analyzer
        }
        if self.comment is not None:
            data["comment"] = self.comment
        if self.external_issues:
            data["externalSystemIssues"] = self.external_issues
        return data
