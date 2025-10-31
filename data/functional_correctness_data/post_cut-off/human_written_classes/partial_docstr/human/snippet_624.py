from wave_lang.support.ir_imports import Block, FloatAttr, InsertionPoint, IntegerAttr, IrType, Operation, OpResult, RankedTensorType, StringAttr, SymbolTable, Value

class Pass:
    """Minimal Pass base class for custom op expansion."""

    def __init__(self, root_op: Operation):
        self.root_op = root_op

    def run(self):
        raise NotImplementedError

    @property
    def funcs(self):
        """Get all func.func operations in the module."""
        results = []
        for region in self.root_op.regions:
            for block in region.blocks:
                for op in block.operations:
                    actual_op = op.operation
                    if actual_op.name == 'func.func':
                        results.append(type('OpMatchResult', (), {'op': op})())
        return results

    def erase_unused_op(self, op: Operation):
        """Recursively erases any unused torch ops, starting with op."""
        from wave_lang.support.ir_imports import OpResult
        worklist = set()
        worklist.add(op)
        while worklist:
            ops = worklist
            worklist = set()
            for op in ops:
                if not self._is_erasable_value_op(op):
                    continue
                if not self._op_is_live(op):
                    for operand in op.operands:
                        if OpResult.isinstance(operand):
                            worklist.add(operand.owner)
                    op.erase()

    def _is_erasable_value_op(self, op: Operation):
        name = op.name
        return name.startswith('torch.') or name.startswith('torch_c.')

    def _op_is_live(self, op: Operation) -> bool:
        for r in op.results:
            try:
                next(r.uses)
                return True
            except StopIteration:
                pass
        return False