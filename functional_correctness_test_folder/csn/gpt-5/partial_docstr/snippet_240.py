class ExternalIssue:
    '''This class represents external(BTS) system issue.'''

    def __init__(self, bts_url=None, bts_project=None, submit_date=None, ticket_id=None, url=None):
        self.bts_url = bts_url
        self.bts_project = bts_project
        self.submit_date = submit_date
        self.ticket_id = ticket_id
        self.url = url

    @property
    def payload(self):
        def _serialize_date(value):
            try:
                # Support datetime/date conversion to ISO format
                from datetime import datetime, date
                if isinstance(value, (datetime, date)):
                    return value.isoformat()
            except Exception:
                pass
            return value

        return {
            'bts_url': self.bts_url,
            'bts_project': self.bts_project,
            'submit_date': _serialize_date(self.submit_date),
            'ticket_id': self.ticket_id,
            'url': self.url,
        }
