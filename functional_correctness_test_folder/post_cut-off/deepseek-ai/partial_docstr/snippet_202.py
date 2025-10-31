
from typing import List, Optional, Iterable
from pip._internal.index.collector import InstallationCandidate


class BestCandidateResult:

    def __init__(self, candidates: List[InstallationCandidate], applicable_candidates: List[InstallationCandidate], best_candidate: Optional[InstallationCandidate]) -> None:
        self._candidates = candidates
        self._applicable_candidates = applicable_candidates
        self._best_candidate = best_candidate

    def iter_all(self) -> Iterable[InstallationCandidate]:
        return iter(self._candidates)

    def iter_applicable(self) -> Iterable[InstallationCandidate]:
        return iter(self._applicable_candidates)
