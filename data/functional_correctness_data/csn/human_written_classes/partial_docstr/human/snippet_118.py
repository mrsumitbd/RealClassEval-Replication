from copy import copy
from mythril.laser.smt import SMTBool as Bool
from mythril.laser.ethereum.state.global_state import GlobalState

class OverUnderflowAnnotation:
    """Symbol Annotation used if a BitVector can overflow"""

    def __init__(self, overflowing_state: GlobalState, operator: str, constraint: Bool) -> None:
        self.overflowing_state = overflowing_state
        self.operator = operator
        self.constraint = constraint

    def __deepcopy__(self, memodict={}):
        new_annotation = copy(self)
        return new_annotation