from typing import Tuple
from pipask.cli_helpers import SimpleTaskProgress
from pipask.checks.base_checker import Checker
from pipask.checks.types import CheckResult, CheckResultType, PackageCheckResults

class _CheckProgressTracker:

    def __init__(self, progress: SimpleTaskProgress, checkers_with_counts: list[Tuple[Checker, int]]):
        self._progress = progress
        self._progress_tasks_by_checker = {id(checker): progress.add_task(checker.description, total=total_count) for checker, total_count in checkers_with_counts}

    def update_all_checks(self, partial_result: bool | CheckResultType):
        for progress_task in self._progress_tasks_by_checker.values():
            progress_task.update(partial_result)

    def update_check(self, checker: Checker, partial_result: bool | CheckResultType):
        progress_task = self._progress_tasks_by_checker.get(id(checker))
        if progress_task is None:
            logger.warning(f'No progress task found for checker {checker}')
            return
        progress_task.update(partial_result)