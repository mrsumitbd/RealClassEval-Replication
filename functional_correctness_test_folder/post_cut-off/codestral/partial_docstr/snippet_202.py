
from typing import List, Optional, Iterable


class InstallationCandidate:
    pass


class BestCandidateResult:

    def __init__(self, candidates: List[InstallationCandidate], applicable_candidates: List[InstallationCandidate], best_candidate: Optional[InstallationCandidate]) -> None:
        self.candidates = candidates
        self.applicable_candidates = applicable_candidates
        self.best_candidate = best_candidate

    def iter_all(self) -> Iterable[InstallationCandidate]:
        return iter(self.candidates)

    def iter_applicable(self) -> Iterable[InstallationCandidate]:
        return iter(self.applicable_candidates)
