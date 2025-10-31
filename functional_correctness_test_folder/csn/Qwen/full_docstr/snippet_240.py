
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
        return {
            'bts_url': self.bts_url,
            'bts_project': self.bts_project,
            'submit_date': self.submit_date,
            'ticket_id': self.ticket_id,
            'url': self.url
        }
