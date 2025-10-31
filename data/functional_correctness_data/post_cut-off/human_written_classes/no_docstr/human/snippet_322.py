import click

class TorrentClient:

    def __init__(self, username, password, url=None, scheme=None, host=None, port=None):
        self.username = username
        self.password = password
        self.url = url
        self.scheme = scheme
        self.host = host
        self.port = port
        click.secho(f'Initializing {self.__class__.__name__} client...', fg='cyan')
        self.client = self.login()

    def login(self):
        raise NotImplementedError

    def add_to_downloader(self, remote_folder, torrent, is_paused, label):
        raise NotImplementedError