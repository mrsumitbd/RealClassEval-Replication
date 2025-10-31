from math import ceil
from apio.utils import util
from apio.common.apio_styles import ERROR
from rich.progress import track
from apio.common.apio_console import cout, console
import requests

class FileDownloader:
    """Class for downloading files"""
    CHUNK_SIZE = 1024

    def __init__(self, url: str, dest_dir=None):
        """Initialize a FileDownloader object
        * INPUTs:
          * url: File to download (full url)
                 (Ex. 'https://github.com/FPGAwars/apio-examples/
                       releases/download/0.0.35/apio-examples-0.0.35.zip')
          * dest_dir: Destination folder (where to download the file)
        """
        self._url = url
        self.fname = url.split('/')[-1]
        self.destination = self.fname
        if dest_dir:
            self.destination = dest_dir / self.fname
        self._request = requests.get(url, stream=True, timeout=TIMEOUT_SECS)
        if self._request.status_code != 200:
            cout(f'Got an unexpected HTTP status code: {self._request.status_code}', f'When downloading {url}', style=ERROR)
            raise util.ApioException()

    def get_size(self) -> int:
        """Return the size (in bytes) of the latest bytes block received"""
        return int(self._request.headers['content-length'])

    def start(self):
        """Start the downloading of the file"""
        itercontent = self._request.iter_content(chunk_size=self.CHUNK_SIZE)
        with open(self.destination, 'wb') as file:
            num_chunks = int(ceil(self.get_size() / float(self.CHUNK_SIZE)))
            for _ in track(range(num_chunks), description='Downloading', console=console()):
                file.write(next(itercontent))
            assert next(itercontent, None) is None
        self._request.close()

    def __del__(self):
        """Close any pending request"""
        if self._request:
            self._request.close()