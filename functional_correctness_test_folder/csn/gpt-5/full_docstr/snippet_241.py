class Issue:
    '''This class represents an issue that can be attached to test result.'''

    _ALLOWED_ISSUE_TYPE_PREFIXES = {"pb", "ab", "si", "ti"}
    _EXTERNAL_ISSUE_FIELDS = {"submitter", "systemId",
                              "ticketId", "url", "btsProject", "btsUrl"}

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
        if not isinstance(issue_type, str):
            raise TypeError("issue_type must be a string")

        issue_type_lc = issue_type.strip().lower()
        if issue_type_lc == "nd001":
            validated_issue_type = "nd001"
        else:
            if len(issue_type_lc) != 5:
                raise ValueError(
                    'issue_type must have format "<prefix><3 digits>", e.g., "pb001" or be "nd001"')
            prefix, digits = issue_type_lc[:2], issue_type_lc[2:]
            if prefix not in self._ALLOWED_ISSUE_TYPE_PREFIXES or not digits.isdigit():
                raise ValueError(
                    'issue_type must start with one of {"pb","ab","si","ti"} followed by 3 digits, or be "nd001"')
            validated_issue_type = issue_type_lc

        self._issue_type = validated_issue_type
        self._comment = None if comment is None else str(comment)
        self._auto_analyzed = bool(auto_analyzed)
        self._ignore_analyzer = bool(ignore_analyzer)
        self._external_system_issues = []

    def external_issue_add(self, issue):
        '''Add external system issue to the issue.'''
        if not isinstance(issue, dict):
            raise TypeError("issue must be a dict")

        # Keep only known fields and coerce to str, drop empty values
        sanitized = {}
        for k in self._EXTERNAL_ISSUE_FIELDS:
            if k in issue and issue[k] is not None:
                val = str(issue[k]).strip()
                if val:
                    sanitized[k] = val

        if not sanitized:
            raise ValueError(
                "External issue must contain at least one supported non-empty field")

        self._external_system_issues.append(sanitized)

    @property
    def payload(self):
        '''Form the correct dictionary for the issue.'''
        data = {
            "issueType": self._issue_type,
            "autoAnalyzed": self._auto_analyzed,
            "ignoreAnalyzer": self._ignore_analyzer,
        }
        if self._comment is not None:
            data["comment"] = self._comment
        if self._external_system_issues:
            data["externalSystemIssues"] = list(self._external_system_issues)
        return data
