class PrologEpilogOp:
    """Meant as an abstract class representing a generic unwind code.
    There is a subclass of PrologEpilogOp for each member of UNWIND_OP_CODES enum.
    """

    def initialize(self, unw_code, data, unw_info, file_offset):
        self.struct = StructureWithBitfields(self._get_format(unw_code), file_offset=file_offset)
        self.struct.__unpack__(data)

    def length_in_code_structures(self, unw_code, unw_info):
        """Computes how many UNWIND_CODE structures UNWIND_CODE occupies.
        May be called before initialize() and, for that reason, should not rely on
        the values of intance attributes.
        """
        return 1

    def is_valid(self):
        return True

    def _get_format(self, unw_code):
        return ('UNWIND_CODE', ('B,CodeOffset', 'B:4,UnwindOp', 'B:4,OpInfo'))