from rich.table import Column
from rich.console import Console
from rich.progress import BarColumn, MofNCompleteColumn, Progress, TaskProgressColumn, TextColumn, TimeRemainingColumn

class RichProgressBar:
    """Display progress bar using rich."""

    def __init__(self, *, console: Console, desc: str, total: float | None=None, unit: str | None=None, unit_scale: float | None=1.0, disable: bool=False, **kwargs):
        self._entered = False
        self.progress = Progress(TextColumn('[progress.description]{task.description}', table_column=Column(min_width=20)), BarColumn(), TaskProgressColumn(), MofNCompleteColumn(), TimeRemainingColumn(), console=console, auto_refresh=True, redirect_stderr=True, redirect_stdout=False, disable=disable, **kwargs)
        self.unit_scale = unit_scale
        self.progress_bar = self.progress.add_task(desc, total=total * self.unit_scale if total is not None and self.unit_scale is not None else None, unit=unit)

    def __enter__(self):
        self.progress.start()
        self._entered = True
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.progress.refresh()
        self.progress.stop()
        return False

    def update(self, n=1, *, completed=None):
        assert self._entered, 'Progress bar must be entered before updating'
        if completed is None:
            advance = self.unit_scale if n is None else n
            self.progress.update(self.progress_bar, advance=advance)
        else:
            self.progress.update(self.progress_bar, completed=completed)