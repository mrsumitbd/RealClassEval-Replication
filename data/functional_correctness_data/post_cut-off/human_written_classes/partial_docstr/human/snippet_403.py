import psutil
import time

class CPUMonitor:
    """Non-blocking CPU monitoring with cgroup awareness."""

    def __init__(self, max_cpu_per_core: float):
        self.process = psutil.Process()
        effective_cores = get_effective_cpus()
        self.max_total_cpu = max_cpu_per_core * effective_cores
        logger.info(f'CPU Monitor: {effective_cores:.1f} effective cores, {self.max_total_cpu:.1f}% limit')
        self.process.cpu_percent(interval=None)
        time.sleep(0.01)
        self.last_check = time.time()
        self.last_cpu = self.process.cpu_percent(interval=None)

    def get_cpu_nowait(self) -> float:
        """Get CPU without blocking."""
        now = time.time()
        if now - self.last_check > 1.0:
            val = self.process.cpu_percent(interval=None)
            if val == 0.0 and self.last_cpu == 0.0:
                time.sleep(0.01)
                val = self.process.cpu_percent(interval=None)
            self.last_cpu = val
            self.last_check = now
        return self.last_cpu

    def should_throttle(self) -> bool:
        """Check if we should throttle based on CPU."""
        return self.get_cpu_nowait() > self.max_total_cpu