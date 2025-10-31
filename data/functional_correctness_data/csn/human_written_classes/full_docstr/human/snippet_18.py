from typing import TYPE_CHECKING, Dict, List
from mythril.laser.ethereum.state.constraints import Constraints

class Node:
    """The representation of a call graph node."""

    def __init__(self, contract_name: str, start_addr=0, constraints=None, function_name='unknown') -> None:
        """

        :param contract_name:
        :param start_addr:
        :param constraints:
        """
        constraints = constraints if constraints else Constraints()
        self.contract_name = contract_name
        self.start_addr = start_addr
        self.states: List[GlobalState] = []
        self.constraints = constraints
        self.function_name = function_name
        self.flags = NodeFlags()
        self.uid = hash(self)

    def get_cfg_dict(self) -> Dict:
        """
        Generate a configuration dictionary for the current state of the contract.

        :return: A dictionary containing the contract's configuration details.
        """
        code_lines = [f"{instruction['address']} {instruction['opcode']}" + (f" {instruction['argument']}" if instruction['opcode'].startswith('PUSH') and 'argument' in instruction else '') for state in self.states for instruction in [state.get_current_instruction()]]
        code = '\\n'.join(code_lines)
        return {'contract_name': self.contract_name, 'start_addr': self.start_addr, 'function_name': self.function_name, 'code': code}