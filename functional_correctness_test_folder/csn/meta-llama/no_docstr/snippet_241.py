
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
        return {
            'type': self.issue_type,
            'comment': self.comment,
            'autoAnalyzed': self.auto_analyzed,
            'ignoreAnalyzer': self.ignore_analyzer,
            'externalIssues': self.external_issues
        }
