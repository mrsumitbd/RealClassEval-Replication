
from __future__ import annotations

from typing import Iterable, List, Optional

# Assume InstallationCandidate is defined elsewhere in the package
# from .candidate import InstallationCandidate


class BestCandidateResult:
    '''A collection of candidates, returned by `PackageFinder.find_best_candidate`.
    This class is only intended to be instantiated by CandidateEvaluator's
    `compute_best_candidate()` method.
    '''

    def __init__(
        self,
        candidates: List[InstallationCandidate],
        applicable_candidates: List[InstallationCandidate],
        best_candidate: Optional[InstallationCandidate],
    ) -> None:
        '''
        :param candidates: A sequence of all available candidates found.
        :param applicable_candidates: The applicable candidates.
        :param best_candidate: The most preferred candidate found, or None
            if no applicable candidates were found.
        '''
        self.candidates = list(candidates)
        self.applicable_candidates = list(applicable_candidates)
        self.best_candidate = best_candidate

    def iter_all(self) -> Iterable[InstallationCandidate]:
        '''Iterate through all candidates.'''
        return iter(self.candidates)

    def iter_applicable(self) -> Iterable[InstallationCandidate]:
        '''Iterate through the applicable candidates.'''
        return iter(self.applicable_candidates)
