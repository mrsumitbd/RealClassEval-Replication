
class Issue:

    def __init__(self, issue_type, comment=None, auto_analyzed=False, ignore_analyzer=True):
        self.issue_type = issue_type
        self.comment = comment
        self.auto_analyzed = auto_analyzed
        self.ignore_analyzer = ignore_analyzer

    def external_issue_add(self, issue):
        self.issue_type = issue.issue_type
        self.comment = issue.comment
        self.auto_analyzed = issue.auto_analyzed
        self.ignore_analyzer = issue.ignore_analyzer

    @property
    def payload(self):
        return {
            'issue_type': self.issue_type,
            'comment': self.comment,
            'auto_analyzed': self.auto_analyzed,
            'ignore_analyzer': self.ignore_analyzer
        }
