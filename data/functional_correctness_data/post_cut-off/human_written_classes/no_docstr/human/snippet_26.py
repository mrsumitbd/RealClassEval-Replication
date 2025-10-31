class BenchmarkedModelKey:
    model: str
    split: str
    step_indices: list[int] | None = None

    def __init__(self, model: str, split: str, step_indices: list[int] | None=None):
        self.model = model
        self.split = split
        self.step_indices = step_indices

    def __str__(self):
        steps_str = ''
        if self.step_indices is not None:
            if len(self.step_indices) == 1:
                steps_str = f'{self.step_indices[0]}'
            else:
                steps_str = f'{self.step_indices[0]}-{self.step_indices[-1]}'
        return f'{self.model} {self.split} {steps_str}'