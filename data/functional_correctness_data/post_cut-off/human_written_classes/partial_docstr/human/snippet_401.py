from math import gcd
from typing import Dict, List, Tuple, Callable, Any, Optional, Union
from functools import reduce

class DimSliceInfo:
    """
    A class to represent the slice information of a tensor along a specific dimension.
    This class contains the offset, total size, dimension name, and length of the slice.
    """
    offset: int
    total_size: int
    dim: str
    length: int = 1

    def __init__(self, offset: int, total_size: int, dim: str='', length: int=1):
        """
        Initialize the DimSliceInfo with the given offset, total size, dimension name, and length.
        """
        self.offset = offset
        self.total_size = total_size
        self.dim = dim
        self.length = length

    def __repr__(self):
        return f'{self.__dict__}'

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """
        Create a DimSliceInfo object from a dictionary.
        :param data: A dictionary containing the keys 'offset', 'total_size', 'dim', and 'length'.
        :return: A DimSliceInfo object.
        """
        return DimSliceInfo(offset=data['offset'], total_size=data['total_size'], dim=data.get('dim', ''), length=data.get('length', 1))

    def simplify(self):
        common = reduce(gcd, [self.offset, self.total_size, self.length])
        return DimSliceInfo(offset=self.offset // common, total_size=self.total_size // common, dim=self.dim, length=self.length // common)