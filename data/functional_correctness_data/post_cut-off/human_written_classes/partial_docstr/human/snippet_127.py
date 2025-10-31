from typing import Any, Dict, List, Optional, Union, Literal, Annotated

class ParallelWorkerBase:
    """Base class for objects that can be parallelized across multiple worker processes.

    This class defines the standard lifecycle for parallel processing:

    Main Process:
        1. init() - Initialize the object in the main process
        2. spawn workers and call init_worker() in each worker
        3. run() - Execute the main workload in parallel across workers
        4. teardown_worker() - Clean up resources in each worker
        5. teardown() - Final cleanup in the main process

    Subclasses should implement the run() method and optionally override
    the lifecycle methods for custom initialization and cleanup behavior.
    """

    def __init__(self) -> None:
        """Initialize the base class. This method can be overridden by subclasses."""
        self.worker_id: Optional[int] = None

    def init(self, *args: Any, **kwargs: Any) -> None:
        pass

    def init_worker(self, worker_id: int, *args: Any, **kwargs: Any) -> None:
        self.worker_id = worker_id

    def run(self, *args: Any, **kwargs: Any) -> Any:
        pass

    def teardown_worker(self, worker_id: int, *args: Any, **kwargs: Any) -> None:
        pass

    def teardown(self, *args: Any, **kwargs: Any) -> None:
        pass