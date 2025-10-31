from nornir.core.task import AggregatedResult, Task
from typing import List
from concurrent.futures import ThreadPoolExecutor
from nornir.core.inventory import Host

class ThreadedRunner:
    """
    ThreadedRunner runs the task over each host using threads

    Arguments:
        num_workers: number of threads to use
    """

    def __init__(self, num_workers: int=20) -> None:
        self.num_workers = num_workers

    def run(self, task: Task, hosts: List[Host]) -> AggregatedResult:
        result = AggregatedResult(task.name)
        futures = []
        with ThreadPoolExecutor(self.num_workers) as pool:
            for host in hosts:
                future = pool.submit(task.copy().start, host)
                futures.append(future)
        for future in futures:
            worker_result = future.result()
            result[worker_result.host.name] = worker_result
        return result