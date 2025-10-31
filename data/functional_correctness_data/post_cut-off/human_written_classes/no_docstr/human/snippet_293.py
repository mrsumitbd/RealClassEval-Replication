from collections.abc import Iterator
from fraim.inputs.chunks import chunk_input
from fraim.core.contextuals.code import CodeChunk
from fraim.inputs.file import BufferedFile

class ProjectInputFileChunker:

    def __init__(self, file: BufferedFile, project_path: str, chunk_size: int) -> None:
        self.file = file
        self.project_path = project_path
        self.chunk_size = chunk_size

    def __iter__(self) -> Iterator[CodeChunk]:
        return chunk_input(self.file, self.chunk_size)