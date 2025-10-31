import z3
from mythril.laser.smt.bitvec import BitVec
from typing import cast

class BaseArray:
    """Base array type, which implements basic store and set operations."""

    def __init__(self, raw):
        self.raw = raw

    def __getitem__(self, item: BitVec) -> BitVec:
        """Gets item from the array, item can be symbolic."""
        if isinstance(item, slice):
            raise ValueError('Instance of BaseArray, does not support getitem with slices')
        return BitVec(cast(z3.BitVecRef, z3.Select(self.raw, item.raw)))

    def __setitem__(self, key: BitVec, value: BitVec) -> None:
        """Sets an item in the array, key can be symbolic."""
        self.raw = z3.Store(self.raw, key.raw, value.raw)

    def substitute(self, original_expression, new_expression):
        """

        :param original_expression:
        :param new_expression:
        """
        if self.raw is None:
            return
        original_z3 = original_expression.raw
        new_z3 = new_expression.raw
        self.raw = z3.substitute(self.raw, (original_z3, new_z3))