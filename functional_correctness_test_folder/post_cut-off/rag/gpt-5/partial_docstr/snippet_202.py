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
        # Sanity checks to ensure consistency
        assert all(
            a in candidates for a in applicable_candidates), "Applicable candidates must be a subset of all candidates."
        if best_candidate is not None:
            assert best_candidate in applicable_candidates, "Best candidate must be among applicable candidates."

        # Store as tuples to discourage mutation
        self._candidates: tuple[InstallationCandidate, ...] = tuple(candidates)
        self._applicable_candidates: tuple[InstallationCandidate, ...] = tuple(
            applicable_candidates)
        self.best_candidate: Optional[InstallationCandidate] = best_candidate

    def iter_all(self) -> Iterable[InstallationCandidate]:
        '''Iterate through all candidates.'''
        return iter(self._candidates)

    def iter_applicable(self) -> Iterable[InstallationCandidate]:
        '''Iterate through the applicable candidates.'''
        return iter(self._applicable_candidates)
