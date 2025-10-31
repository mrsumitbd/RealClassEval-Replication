from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, TypedDict, Union, cast
from src.exceptions import ContextError
from dataclasses import asdict, dataclass, field, fields

@dataclass(slots=True)
class TimingParameters:
    """Device timing parameters."""
    read_latency: int
    write_latency: int
    burst_length: int
    inter_burst_gap: int
    timeout_cycles: int
    clock_frequency_mhz: float
    timing_regularity: float

    def __post_init__(self):
        """Validate timing parameters."""
        for field_obj in fields(self):
            value = getattr(self, field_obj.name)
            if value is None:
                raise ContextError(f'{field_obj.name} cannot be None')
            if value <= 0:
                raise ContextError(f'{field_obj.name} must be positive: {value}')
        if not 0 < self.timing_regularity <= 1.0:
            raise ContextError(f'Invalid timing_regularity: {self.timing_regularity}')

    @property
    def total_latency(self) -> int:
        """Calculate total latency."""
        return self.read_latency + self.write_latency

    @property
    def effective_bandwidth_mbps(self) -> float:
        """Estimate bandwidth in MB/s."""
        cycles_per_burst = self.burst_length + self.inter_burst_gap
        bursts_per_second = self.clock_frequency_mhz * 1000000.0 / cycles_per_burst
        bytes_per_burst = self.burst_length * 4
        return bursts_per_second * bytes_per_burst / 1000000.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = asdict(self)
        result.update({'total_latency': self.total_latency, 'effective_bandwidth_mbps': self.effective_bandwidth_mbps})
        return result