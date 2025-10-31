from pathlib import Path
from multiprocessing import Pool, cpu_count
import json
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

class ParallelJsonDumper:

    def __init__(self, parallel_field: str, chunk_size: int=5000):
        self.chunk_size = chunk_size
        self.cpu_count = cpu_count()
        self.parallel_field = parallel_field

    def dump(self, data: Dict[str, Any], output_path: Path) -> None:
        """Dump JSON with parallel processing of large parallel_field field"""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        pvalue = data.pop(self.parallel_field)
        chunks = self._chunkify_list(pvalue)
        with Pool(processes=min(len(chunks), self.cpu_count)) as pool:
            chunk_strings = pool.map(self._process_chunk, chunks)
            self._write_output(data, chunk_strings, output_path)

    def _chunkify_list(self, pvalue: List[Any]) -> List[List[Any]]:
        """Split list into chunks for parallel processing"""
        return [pvalue[i:i + self.chunk_size] for i in range(0, len(pvalue), self.chunk_size)]

    def _process_chunk(self, chunk: List[Any]) -> str:
        """Convert chunk to JSON and strip enclosing brackets"""
        chunk_json = json.dumps(chunk, separators=(',', ':'))
        return chunk_json[1:-1]

    def _write_output(self, base_data: Dict[str, Any], chunk_strings: List[str], output_path: Path) -> None:
        """Write JSON to disk with proper structure"""
        with open(output_path, 'w') as f:
            f.write(json.dumps(base_data, separators=(',', ':'))[:-1])
            f.write(f',"{self.parallel_field}":[')
            for i, chunk_str in enumerate(chunk_strings):
                if i > 0:
                    f.write(',')
                f.write(chunk_str)
            f.write(']}')