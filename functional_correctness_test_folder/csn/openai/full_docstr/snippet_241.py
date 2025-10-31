
import re
from typing import Any, Dict, List, Optional, Union


class Issue:
    """This class represents an issue that can be attached to a test result."""

    _TYPE_PATTERN = re.compile(r"^(pb|ab|si|ti)\d{3}$")
    _ALLOWED_TYPES = {"nd001"}

    def __init__(
        self,
        issue_type: str,
        comment: Optional[str] = None,
        auto_analyzed: bool = False,
        ignore_analyzer: bool = True,
    ):
        """
        Initialize instance attributes.

        :param issue_type: Issue type locator. Allowable values: "pb***",
                           "ab***", "si***", "ti***", "nd001". Where ***
                           is locator id.
        :param comment: Issue comments
        :param auto_analyzed: Indicator that the issue has been marked with
                              the RP auto analyzer
        :param ignore_analyzer: Flag that forces RP analyzer to ignore this
                                issue
        """
        if not self._is_valid_issue_type(issue_type):
            raise ValueError(
                f"Invalid issue_type '{issue_type}'. "
                f"Allowed patterns: 'pb***', 'ab***', 'si***', 'ti***', 'nd001'."
            )
        self.issue_type: str = issue_type
        self.comment: Optional[str] = comment
        self.auto_analyzed: bool = bool(auto_analyzed)
        self.ignore_analyzer: bool = bool(ignore_analyzer)
        self._external_issues: List[Dict[str, Any]] = []

    @staticmethod
    def _is_valid_issue_type(issue_type: str) -> bool:
        return bool(Issue._TYPE_PATTERN.match(issue_type)) or issue_type in Issue._ALLOWED_TYPES

    def external_issue_add(self, issue: Union[str, Dict[str, Any]]) -> None:
        """
        Add external system issue to the issue.

        :param issue: External issue representation. Can be a string (issue id)
                      or a dictionary containing issue details.
        """
        if isinstance(issue, str):
            issue_dict = {"id": issue}
        elif isinstance(issue, dict):
            issue_dict = issue
        else:
            raise TypeError("External issue must be a string or a dictionary.")
        self._external_issues.append(issue_dict)

    @property
    def payload(self) -> Dict[str, Any]:
        """
        Form the correct dictionary for the issue.

        :return: Dictionary representation suitable for serialization.
        """
        payload: Dict[str, Any] = {
            "issue_type": self.issue_type,
            "auto_analyzed": self.auto_analyzed,
            "ignore_analyzer": self.ignore_analyzer,
        }
        if self.comment is not None:
            payload["comment"] = self.comment
        if self._external_issues:
            payload["external_issues"] = list(self._external_issues)
        return payload
