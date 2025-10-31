
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
        self.issue_type = issue_type
        self.comment = comment
        self.auto_analyzed = auto_analyzed
        self.ignore_analyzer = ignore_analyzer
        self.external_issues = []

    def external_issue_add(self, issue):
        self.external_issues.append(issue)

    @property
    def payload(self):
        '''Form the correct dictionary for the issue.'''
        payload = {
            'issueType': self.issue_type,
            'comment': self.comment,
            'autoAnalyzed': self.auto_analyzed,
            'ignoreAnalyzer': self.ignore_analyzer
        }
        if self.external_issues:
            payload['externalIssues'] = self.external_issues
        return payload
