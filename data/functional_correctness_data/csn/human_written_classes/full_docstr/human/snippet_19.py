class StateAnnotation:
    """The StateAnnotation class is used to persist information over traces.

    This allows modules to reason about traces without the need to
    traverse the state space themselves.
    """

    @property
    def persist_to_world_state(self) -> bool:
        """If this function returns true then laser will also annotate the
        world state.

        If you want annotations to persist through different user initiated message call transactions
        then this should be enabled.

        The default is set to False
        """
        return False

    @property
    def persist_over_calls(self) -> bool:
        """If this function returns true then laser will propagate the annotation between calls

        The default is set to False
        """
        return False

    @property
    def search_importance(self) -> int:
        """
        Used in estimating the priority of a state annotated with the corresponding annotation.
        Default is 1
        """
        return 1