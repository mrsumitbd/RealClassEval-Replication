from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

@dataclass
class BatchProcessingResult:
    """Result of batch processing operation"""
    successful_files: List[str]
    failed_files: List[str]
    total_files: int
    processing_time: float
    errors: Dict[str, str]
    output_dir: str

    @property
    def success_rate(self) -> float:
        """Calculate success rate as percentage"""
        if self.total_files == 0:
            return 0.0
        return len(self.successful_files) / self.total_files * 100

    def summary(self) -> str:
        """Generate a summary of the batch processing results"""
        return f'Batch Processing Summary:\n  Total files: {self.total_files}\n  Successful: {len(self.successful_files)} ({self.success_rate:.1f}%)\n  Failed: {len(self.failed_files)}\n  Processing time: {self.processing_time:.2f} seconds\n  Output directory: {self.output_dir}'