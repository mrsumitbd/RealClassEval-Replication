class Report:

    def __init__(self, expiration_datetime, id, launch_datetime, output_format, size, status, type, user_login, title=''):
        self.expiration_datetime = str(expiration_datetime).replace('T', ' ').replace('Z', '').split(' ')
        self.id = int(id)
        self.launch_datetime = str(launch_datetime).replace('T', ' ').replace('Z', '').split(' ')
        self.output_format = output_format
        self.size = size
        self.status = status.STATE
        self.type = type
        self.user_login = user_login
        self.title = title

    def __repr__(self):
        return f'qualys_id: {self.id}, title: {self.title}'

    def download(self, conn):
        call = '/api/2.0/fo/report'
        parameters = {'action': 'fetch', 'id': self.id}
        if self.status == 'Finished':
            return conn.request(call, parameters)