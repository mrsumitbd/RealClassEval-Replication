from nornir.core.task import AggregatedResult, Task
from typing import List
from nornir.core.inventory import Host

class SerialRunner:
    """
    SerialRunner runs the task over each host one after the other without any parellelization
    """

    def __init__(self) -> None:
        pass

    def run(self, task: Task, hosts: List[Host]) -> AggregatedResult:
        result = AggregatedResult(task.name)
        for host in hosts:
            result[host.name] = task.copy().start(host)
        return result