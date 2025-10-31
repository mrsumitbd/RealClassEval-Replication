
from typing import List, Iterable, Optional


class BestCandidateResult:
    """
    Holds the result of a best‑candidate search.

    Attributes
    ----------
    candidates : List[InstallationCandidate]
        All candidates that were considered.
    applicable_candidates : List[InstallationCandidate]
        Candidates that are applicable to the current environment.
    best_candidate : Optional[InstallationCandidate]
        The best candidate found, or None if no applicable candidate exists.
    """

    def __init__(
        self,
        candidates: List["InstallationCandidate"],
        applicable_candidates: List["InstallationCandidate"],
        best_candidate: Optional["InstallationCandidate"],
    ) -> None:
        self.candidates = candidates
        self.applicable_candidates = applicable_candidates
        self.best_candidate = best_candidate

    def iter_all(self) -> Iterable["InstallationCandidate"]:
        """Iterate over all candidates."""
        return iter(self.candidates)

    def iter_applicable(self) -> Iterable["InstallationCandidate"]:
        """Iterate over applicable candidates."""
        return iter(self.applicable_candidates)
