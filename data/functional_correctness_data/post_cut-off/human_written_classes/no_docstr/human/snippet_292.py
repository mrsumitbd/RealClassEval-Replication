from fraim.inputs.input import Input
from fraim.inputs.git import GitRemote
from fraim.inputs.local import Local
import logging
from fraim.inputs.git_diff import GitDiff
from typing import Any
from collections.abc import Iterator
from fraim.core.contextuals.code import CodeChunk
import os

class ProjectInput:
    input: Input
    chunk_size: int
    project_path: str
    repo_name: str
    chunker: type['ProjectInputFileChunker']

    def __init__(self, logger: logging.Logger, kwargs: Any) -> None:
        self.logger = logger
        path_or_url = kwargs.location or None
        globs = kwargs.globs
        limit = kwargs.limit
        self.chunk_size = kwargs.chunk_size
        self.base = kwargs.base
        self.head = kwargs.head
        self.diff = kwargs.diff
        self.chunker = ProjectInputFileChunker
        if path_or_url is None:
            raise ValueError('Location is required')
        if path_or_url.startswith('http://') or path_or_url.startswith('https://') or path_or_url.startswith('git@'):
            self.repo_name = path_or_url.split('/')[-1].replace('.git', '')
            self.input = GitRemote(self.logger, url=path_or_url, globs=globs, limit=limit, prefix='fraim_scan_')
            self.project_path = self.input.root_path()
        else:
            self.project_path = os.path.abspath(path_or_url)
            self.repo_name = os.path.basename(self.project_path)
            if self.diff:
                self.input = GitDiff(self.project_path, head=self.head, base=self.base, globs=globs, limit=limit)
            else:
                self.input = Local(self.logger, self.project_path, globs=globs, limit=limit)

    def __iter__(self) -> Iterator[CodeChunk]:
        yield from self.input