from salmon.uploader.torrent_client import TorrentClientGenerator

class Uploader:

    def __init__(self, url, extra_args, client):
        self.url = url
        self.extra_args = extra_args
        self.client = TorrentClientGenerator.parse_libtc_url(client)

    def upload_folder(self, remote_folder, path, type):
        raise NotImplementedError

    def add_to_downloader(self, remote_folder, path, type, label, add_paused):
        raise NotImplementedError