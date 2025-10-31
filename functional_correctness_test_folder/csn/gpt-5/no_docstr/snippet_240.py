class ExternalIssue:
    def __init__(self, bts_url=None, bts_project=None, submit_date=None, ticket_id=None, url=None):
        self.bts_url = bts_url
        self.bts_project = bts_project
        self._submit_date = submit_date
        self.ticket_id = ticket_id
        self.url = url

    def _normalize_submit_date(self, value):
        if value is None:
            return None
        try:
            import datetime as _dt
            if isinstance(value, _dt.datetime):
                return value.isoformat()
            if isinstance(value, _dt.date):
                return value.isoformat()
            if isinstance(value, (int, float)):
                return _dt.datetime.fromtimestamp(value, _dt.timezone.utc).isoformat()
            if isinstance(value, str):
                # If it's already a string, keep as-is
                return value
        except Exception:
            pass
        return str(value)

    @property
    def payload(self):
        data = {
            "bts_url": self.bts_url,
            "bts_project": self.bts_project,
            "submit_date": self._normalize_submit_date(self._submit_date),
            "ticket_id": self.ticket_id,
            "url": self.url,
        }
        return {k: v for k, v in data.items() if v is not None}
