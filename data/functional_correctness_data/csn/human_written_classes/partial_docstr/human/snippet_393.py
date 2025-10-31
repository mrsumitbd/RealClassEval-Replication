from apio.utils import util

class ArchiveBase:
    """DOC: TODO"""

    def __init__(self, arhfileobj, is_tar_file: bool):
        self._afo = arhfileobj
        self._is_tar_file = is_tar_file

    def get_items(self):
        """DOC: TODO"""
        raise NotImplementedError()

    def extract_item(self, item, dest_dir):
        """DOC: TODO"""
        if hasattr(item, 'filename') and item.filename.endswith('.gitignore'):
            return
        if self._is_tar_file and util.get_python_ver_tuple() >= (3, 12, 0):
            self._afo.extract(item, dest_dir, filter='fully_trusted')
        else:
            self._afo.extract(item, dest_dir)
        self.after_extract(item, dest_dir)

    def after_extract(self, item, dest_dir):
        """DOC: TODO"""