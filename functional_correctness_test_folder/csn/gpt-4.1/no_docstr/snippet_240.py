
class ExternalIssue:

    def __init__(self, bts_url=None, bts_project=None, submit_date=None, ticket_id=None, url=None):
        self.bts_url = bts_url
        self.bts_project = bts_project
        self.submit_date = submit_date
        self.ticket_id = ticket_id
        self.url = url

    @property
    def payload(self):
        return {
            "bts_url": self.bts_url,
            "bts_project": self.bts_project,
            "submit_date": self.submit_date,
            "ticket_id": self.ticket_id,
            "url": self.url
        }
