
from typing import List, Optional, Iterable


class InstallationCandidate:
    # Assuming InstallationCandidate is defined elsewhere
    pass


class BestCandidateResult:

    def __init__(self, candidates: List[InstallationCandidate], applicable_candidates: List[InstallationCandidate], best_candidate: Optional[InstallationCandidate]) -> None:
        '''
        :param candidates: A sequence of all available candidates found.
        :param applicable_candidates: The applicable candidates.
        :param best_candidate: The most preferred candidate found, or None
            if no applicable candidates were found.
        '''
        self.candidates = candidates
        self.applicable_candidates = applicable_candidates
        self.best_candidate = best_candidate

    def iter_all(self) -> Iterable[InstallationCandidate]:
        return iter(self.candidates)

    def iter_applicable(self) -> Iterable[InstallationCandidate]:
        return iter(self.applicable_candidates)
