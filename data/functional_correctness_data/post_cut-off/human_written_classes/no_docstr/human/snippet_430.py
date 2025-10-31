import shutil
from os import PathLike
import os.path
import requests
from io import BytesIO
import zipfile

class DataSource:
    url = None
    name = None
    hash = None

    def __init__(self):
        self.out_folder = os.path.expanduser(f'~/annflux/datasources/{self.name}')
        print(self.out_folder)
        if not os.path.isdir(self.out_folder):
            self.download()

    def download(self):
        if self.url is None:
            return
        req = requests.get(self.url)
        zipfile_ = zipfile.ZipFile(BytesIO(req.content))
        zipfile_.extractall(self.out_folder)
        logger.warning(f'Extracted zip to {self.out_folder}')

    @property
    def folder(self):
        return self.out_folder

    def copy_to(self, folder: str | PathLike):
        print(self.out_folder)
        shutil.copytree(self.out_folder, folder)
        logger.warning(f'Copied to {self.out_folder}')