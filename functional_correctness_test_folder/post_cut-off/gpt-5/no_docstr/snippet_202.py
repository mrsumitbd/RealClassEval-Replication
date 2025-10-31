from typing import Iterable, List, Optional, Tuple


class BestCandidateResult:
    def __init__(
        self,
        candidates: List["InstallationCandidate"],
        applicable_candidates: List["InstallationCandidate"],
        best_candidate: Optional["InstallationCandidate"],
    ) -> None:
        self._candidates: Tuple["InstallationCandidate", ...] = tuple(
            candidates)
        self._applicable_candidates: Tuple["InstallationCandidate", ...] = tuple(
            applicable_candidates)
        self.best_candidate: Optional["InstallationCandidate"] = best_candidate

    def iter_all(self) -> Iterable["InstallationCandidate"]:
        return iter(self._candidates)

    def iter_applicable(self) -> Iterable["InstallationCandidate"]:
        return iter(self._applicable_candidates)
