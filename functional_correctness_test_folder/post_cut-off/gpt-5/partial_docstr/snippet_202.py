from typing import Iterable, List, Optional, Tuple


class BestCandidateResult:

    def __init__(self, candidates: List['InstallationCandidate'], applicable_candidates: List['InstallationCandidate'], best_candidate: Optional['InstallationCandidate']) -> None:
        '''
        :param candidates: A sequence of all available candidates found.
        :param applicable_candidates: The applicable candidates.
        :param best_candidate: The most preferred candidate found, or None
            if no applicable candidates were found.
        '''
        self.candidates: Tuple['InstallationCandidate', ...] = tuple(
            candidates)
        self.applicable_candidates: Tuple['InstallationCandidate', ...] = tuple(
            applicable_candidates)
        self.best_candidate: Optional['InstallationCandidate'] = best_candidate

    def iter_all(self) -> Iterable['InstallationCandidate']:
        return iter(self.candidates)

    def iter_applicable(self) -> Iterable['InstallationCandidate']:
        return iter(self.applicable_candidates)
