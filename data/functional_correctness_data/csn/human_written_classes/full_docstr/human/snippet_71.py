from pathlib import Path
from apio.utils import util
from rich.progress import track
from apio.common.apio_console import console, cerror

class FileUnpacker:
    """Class for unpacking compressed files"""

    def __init__(self, archpath: Path, dest_dir=Path('.')):
        """Initialize the unpacker object
        * INPUT:
          - archpath: filename with path to uncompress
          - des_dir: Destination folder
        """
        self._archpath = archpath
        self._dest_dir = dest_dir
        self._unpacker = None
        arch_ext = archpath.suffix
        if arch_ext in '.tgz':
            self._unpacker = TARArchive(archpath)
        if not self._unpacker:
            cerror(f"Can not unpack file '{archpath}'")
            raise util.ApioException()

    def start(self) -> bool:
        """Start unpacking the file"""
        items = self._unpacker.get_items()
        for i in track(range(len(items)), description='Unpacking  ', console=console()):
            self._unpacker.extract_item(items[i], self._dest_dir)
        return True