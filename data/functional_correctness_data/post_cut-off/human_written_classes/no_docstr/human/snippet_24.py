from tqdm import auto as tqdm
from collections import Counter
from dataclasses import dataclass, field

@dataclass
class GatherContext:
    pbar: tqdm.tqdm | None = None
    metric_sums: Counter[str] = field(default_factory=Counter)
    metric_divisors: Counter[str] = field(default_factory=Counter)
    max_metrics: int | None = None
    pbar_total_completion_tokens: bool = False
    max_exceptions: int | float = 0
    increment_pbar: bool = True

    def update_pbar(self, n: int) -> None:
        if self.pbar is None:
            return
        if self.increment_pbar:
            self.pbar.update(n)
        postfix = {}
        included_metrics = self.metric_sums.keys()
        if self.max_metrics is not None:
            included_metrics = list(self.metric_sums.keys())[:self.max_metrics]
        for metric in included_metrics:
            sum = self.metric_sums[metric]
            divisor = max(1, self.metric_divisors[metric])
            postfix[metric] = sum / divisor
        for key in ('prompt_tokens', 'completion_tokens', 'total_completion_tokens'):
            if key in postfix:
                postfix[key] = postfix.pop(key)
        self.pbar.set_postfix(postfix)

    def too_many_exceptions(self) -> bool:
        if 0 < self.max_exceptions < 1 and self.pbar is not None and (self.metric_sums['exceptions'] / self.pbar.total <= self.max_exceptions) or self.metric_sums['exceptions'] <= self.max_exceptions:
            return False
        return True

    def reset(self) -> None:
        self.pbar = None
        self.metric_sums = Counter()
        self.metric_divisors = Counter()
        self.pbar_total_completion_tokens = False
        self.max_exceptions = 0