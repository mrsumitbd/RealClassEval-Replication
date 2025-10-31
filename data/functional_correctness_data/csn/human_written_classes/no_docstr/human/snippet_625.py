from tempfile import mkdtemp
import shutil
from typing import Optional
import git

class GitStorage:

    def __init__(self, remote_url: str, revision: Optional[str]=None):
        assert remote_url is not None
        self._remote_url = remote_url
        self._revision = revision
        self._temp_folder = mkdtemp()

    @property
    def temp_folder(self) -> str:
        return self._temp_folder

    def extract(self):
        multi_options = ['--depth', '1']
        if self._revision is not None:
            multi_options.extend(['--branch', self._revision])
        git.Repo.clone_from(self._remote_url, self._temp_folder, multi_options=multi_options)

    def close(self):
        shutil.rmtree(self._temp_folder, ignore_errors=True)