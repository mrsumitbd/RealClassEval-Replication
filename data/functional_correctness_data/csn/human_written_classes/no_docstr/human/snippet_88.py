from mythril.support.support_utils import get_code_hash

class CoverageData:

    def __init__(self, instructions_covered: int, total_instructions: int, branches_covered: int, tx_id: int, total_branches: int, state_counter: int, code: str, time_elapsed: int):
        self.instructions_covered = instructions_covered
        self.total_instructions = total_instructions
        self.branches_covered = branches_covered
        self.tx_id = tx_id
        self.total_branches = total_branches
        self.state_counter = state_counter
        self.code_hash = get_code_hash(code)[2:]
        self.time_elapsed = time_elapsed

    def as_dict(self):
        return self.__dict__