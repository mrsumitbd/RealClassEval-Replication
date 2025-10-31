class ExternalIssue:
    '''This class represents external(BTS) system issue.'''

    def __init__(self, bts_url=None, bts_project=None, submit_date=None, ticket_id=None, url=None):
        '''Initialize instance attributes.
        :param bts_url:     Bug tracker system URL
        :param bts_project: Bug tracker system project
        :param submit_date: Bug submission date
        :param ticket_id:   Unique ID of the ticket at the BTS
        :param url:         URL to the ticket(bug)
        '''
        self.bts_url = bts_url
        self.bts_project = bts_project
        self.submit_date = submit_date
        self.ticket_id = ticket_id
        self.url = url

    @property
    def payload(self):
        '''Form the correct dictionary for the BTS issue.'''
        from datetime import date, datetime

        def _isoformat_date(value):
            if value is None:
                return None
            if isinstance(value, (datetime, date)):
                return value.isoformat()
            return str(value)

        data = {}
        if self.bts_url is not None:
            data['bts_url'] = self.bts_url
        if self.bts_project is not None:
            data['bts_project'] = self.bts_project
        if self.submit_date is not None:
            iso_date = _isoformat_date(self.submit_date)
            if iso_date is not None:
                data['submit_date'] = iso_date
        if self.ticket_id is not None:
            data['ticket_id'] = str(self.ticket_id)
        if self.url is not None:
            data['url'] = self.url
        return dict(data)
