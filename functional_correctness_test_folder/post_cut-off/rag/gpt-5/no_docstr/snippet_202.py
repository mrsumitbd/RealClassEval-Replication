class BestCandidateResult:
    '''A collection of candidates, returned by `PackageFinder.find_best_candidate`.
    This class is only intended to be instantiated by CandidateEvaluator's
    `compute_best_candidate()` method.
    '''

    def __init__(self, candidates: List[InstallationCandidate], applicable_candidates: List[InstallationCandidate], best_candidate: Optional[InstallationCandidate]) -> None:
        '''
        :param candidates: A sequence of all available candidates found.
        :param applicable_candidates: The applicable candidates.
        :param best_candidate: The most preferred candidate found, or None
            if no applicable candidates were found.
        '''
        self._candidates = list(candidates)
        self._applicable_candidates = list(applicable_candidates)
        self.best_candidate = best_candidate

        assert all(
            c in self._candidates for c in self._applicable_candidates), "Applicable candidates must be a subset of all candidates"
        assert best_candidate is None or best_candidate in self._applicable_candidates, "Best candidate must be among applicable candidates"

    def iter_all(self) -> Iterable[InstallationCandidate]:
        '''Iterate through all candidates.'''
        return iter(self._candidates)

    def iter_applicable(self) -> Iterable[InstallationCandidate]:
        '''Iterate through the applicable candidates.'''
        return iter(self._applicable_candidates)
