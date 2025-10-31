import time
from typing import Dict, List, Optional, Any, Set, Tuple, Generator
from pathlib import Path

class IndexingProgress:
    """Track progress toward 100% indexing."""

    def __init__(self, logs_dir: Path):
        self.logs_dir = logs_dir
        self.total_files = 0
        self.indexed_files = 0
        self.start_time = time.time()
        self.last_update = time.time()

    def scan_total_files(self) -> int:
        """Count total JSONL files."""
        total = 0
        if self.logs_dir.exists():
            for project_dir in self.logs_dir.iterdir():
                if project_dir.is_dir():
                    total += len(list(project_dir.glob('*.jsonl')))
        self.total_files = total
        return total

    def update(self, indexed_count: int):
        """Update progress."""
        self.indexed_files = indexed_count
        self.last_update = time.time()

    def get_progress(self) -> Dict[str, Any]:
        """Get progress metrics."""
        percent = min(100.0, self.indexed_files / self.total_files * 100) if self.total_files > 0 else 0
        elapsed = time.time() - self.start_time
        rate = self.indexed_files / elapsed if elapsed > 0 else 0
        remaining = max(0, self.total_files - self.indexed_files)
        eta = remaining / rate if rate > 0 else 0
        return {'total_files': self.total_files, 'indexed_files': min(self.indexed_files, self.total_files), 'percent': percent, 'rate_per_hour': rate * 3600, 'eta_hours': eta / 3600, 'elapsed_hours': elapsed / 3600}