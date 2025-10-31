
class Issue:

    def __init__(self, issue_type, comment=None, auto_analyzed=False, ignore_analyzer=True):
        self.issue_type = issue_type
        self.comment = comment
        self.auto_analyzed = auto_analyzed
        self.ignore_analyzer = ignore_analyzer
        self.external_issues = []

    def external_issue_add(self, issue):
        self.external_issues.append(issue)

    @property
    def payload(self):
        payload = {
            'issue_type': self.issue_type,
            'comment': self.comment,
            'auto_analyzed': self.auto_analyzed,
            'ignore_analyzer': self.ignore_analyzer,
            'external_issues': [issue.payload for issue in self.external_issues]
        }
        return payload
