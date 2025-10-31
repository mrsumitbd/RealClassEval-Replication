from pipask.checks.types import CheckResultType
from rich.progress import Progress, ProgressColumn, Task, TaskID, TextColumn, TimeElapsedColumn

class CheckTask:

    def __init__(self, progress: Progress, task_id: TaskID):
        self._task_id = task_id
        self._progress = progress
        self._result: CheckResultType | None = None

    def update(self, partial_result: bool | CheckResultType):
        if partial_result is True:
            partial_result = CheckResultType.SUCCESS
        elif partial_result is False:
            partial_result = CheckResultType.FAILURE
        self._result = CheckResultType.get_worst(self._result, partial_result)
        self._progress.update(self._task_id, advance=1, result=self._result)

    def show(self):
        self._progress.update(self._task_id, visible=True)
        self._progress.start()

    def hide(self):
        self._progress.update(self._task_id, visible=False)
        self._progress.stop()

    def start(self):
        self._progress.start_task(self._task_id)