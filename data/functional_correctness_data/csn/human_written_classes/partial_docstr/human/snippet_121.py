from mythril.laser.smt import BitVec
from typing import List

class ReturnData:
    """Base returndata class."""

    def __init__(self, return_data: List[BitVec], return_data_size: BitVec) -> None:
        """

        :param tx_id:
        """
        self.return_data = return_data
        self.return_data_size = return_data_size

    @property
    def size(self) -> BitVec:
        """

        :return: Calldata size for this calldata object
        """
        return self.return_data_size

    def __getitem__(self, index):
        if index < self.size:
            return self.return_data[index]
        else:
            return 0