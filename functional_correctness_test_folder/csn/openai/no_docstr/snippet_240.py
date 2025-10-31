
from datetime import datetime
from typing import Any, Dict, Optional


class ExternalIssue:
    """
    Represents an issue in an external bug tracking system.

    Attributes
    ----------
    bts_url : Optional[str]
        Base URL of the bug tracking system.
    bts_project : Optional[str]
        Project identifier within the bug tracking system.
    submit_date : Optional[datetime | str]
        Date the issue was submitted. If a string is provided, it will be parsed
        as an ISO‑8601 datetime.
    ticket_id : Optional[str]
        Identifier of the ticket in the external system.
    url : Optional[str]
        Direct URL to the issue.
    """

    def __init__(
        self,
        bts_url: Optional[str] = None,
        bts_project: Optional[str] = None,
        submit_date: Optional[Any] = None,
        ticket_id: Optional[str] = None,
        url: Optional[str] = None,
    ) -> None:
        self.bts_url = bts_url
        self.bts_project = bts_project

        # Normalize submit_date to datetime if possible
        if isinstance(submit_date, str):
            try:
                self.submit_date = datetime.fromisoformat(submit_date)
            except ValueError:
                # If parsing fails, keep the original string
                self.submit_date = submit_date
        else:
            self.submit_date = submit_date

        self.ticket_id = ticket_id
        self.url = url

    @property
    def payload(self) -> Dict[str, Any]:
        """
        Returns a dictionary representation of the issue suitable for
        serialization or transmission.

        The dictionary includes all attributes, converting datetime objects
        to ISO‑8601 strings.
        """
        payload: Dict[str, Any] = {
            "bts_url": self.bts_url,
            "bts_project": self.bts_project,
            "submit_date": (
                self.submit_date.isoformat()
                if isinstance(self.submit_date, datetime)
                else self.submit_date
            ),
            "ticket_id": self.ticket_id,
            "url": self.url,
        }
        return payload
