
from typing import List, Iterable, Optional


class BestCandidateResult:
    def __init__(
        self,
        candidates: List["InstallationCandidate"],
        applicable_candidates: List["InstallationCandidate"],
        best_candidate: Optional["InstallationCandidate"],
    ) -> None:
        """
        :param candidates: A sequence of all available candidates found.
        :param applicable_candidates: The applicable candidates.
        :param best_candidate: The most preferred candidate found, or None
            if no applicable candidates were found.
        """
        self._candidates = candidates
        self._applicable_candidates = applicable_candidates
        self.best_candidate = best_candidate

    def iter_all(self) -> Iterable["InstallationCandidate"]:
        """Iterate over all candidates."""
        return iter(self._candidates)

    def iter_applicable(self) -> Iterable["InstallationCandidate"]:
        """Iterate over applicable candidates."""
        return iter(self._applicable_candidates)
