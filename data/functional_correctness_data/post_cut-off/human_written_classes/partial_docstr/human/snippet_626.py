from iree.compiler.ir import Context, Location
from dataclasses import dataclass
import inspect
from typing import List, Optional, Union
import sys

@dataclass
class FileLineColInfo:
    """
    Location information containing the filename, line and column.
    """
    filename: str
    line: Union[int, tuple[int, int]]
    col: Union[int, tuple[int, int]]

    def to_mlir(self):
        assert Context.current is not None, 'Must be called under MLIR context manager.'
        line_is_range = isinstance(self.line, tuple)
        col_is_range = isinstance(self.col, tuple)
        if not line_is_range and (not col_is_range):
            return Location.file(self.filename, self.line, self.col)
        line_start = self.line[0] if line_is_range else self.line
        line_end = self.line[1] if line_is_range else self.line
        col_start = self.col[0] if col_is_range else self.col
        col_end = self.col[1] if col_is_range else self.col
        return Location.file(self.filename, line_start, col_start, line_end, col_end)

    @staticmethod
    def capture_current_location():
        for f in inspect.stack():
            if 'wave_lang/kernel' not in f.filename:
                break
        if not f:
            f = inspect.stack()[-1]
        return FileLineColInfo.from_stack_frame(f)

    @staticmethod
    def from_stack_frame(frame: inspect.FrameInfo):
        assert sys.version_info.major == 3, 'Unexpected Python version'
        if sys.version_info.minor < 11:
            return FileLineColInfo(frame.filename, frame.lineno, 0)
        return FileLineColInfo(frame.filename, (frame.positions.lineno, frame.positions.end_lineno), (frame.positions.col_offset, frame.positions.end_col_offset))