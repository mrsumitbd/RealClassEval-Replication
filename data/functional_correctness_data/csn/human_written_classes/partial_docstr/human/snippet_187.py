import urllib.parse as urlparse
from xhtml2pdf.files import getFile
import os

class pisaLinkLoader:
    """
    Helper to load page from an URL and load corresponding
    files to temporary files. If getFileName is called it
    returns the temporary filename and takes care to delete
    it when pisaLinkLoader is unloaded.
    """

    def __init__(self, src, *, quiet=True) -> None:
        self.quiet = quiet
        self.src = src
        self.tfileList: list[str] = []

    def __del__(self) -> None:
        for path in self.tfileList:
            os.remove(path)

    def getFileName(self, name, relative=None):
        url = urlparse.urljoin(relative or self.src, name)
        instance = getFile(url)
        filetmpdownloaded = instance.getNamedFile()
        path = filetmpdownloaded.name
        self.tfileList.append(path)
        if not self.quiet:
            print(f'  Loading {url} to {path}')
        return path