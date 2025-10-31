
from typing import List
import math


class CombinationCalculator:
    """
    This is a class that provides methods to calculate the number of combinations for a specific count, calculate all possible combinations, and generate combinations with a specified number of elements.
    """

    def __init__(self, datas: List[str]):
        """
        Initialize the calculator with a list of data.
        """
        self.datas = datas

    @staticmethod
    def count(n: int, m: int) -> int:
        """
        Calculate the number of combinations for a specific count.
        :param n: The total number of elements,int.
        :param m: The number of elements in each combination,int.
        :return: The number of combinations,int.
        """
        if m > n:
            return 0
        return math.comb(n, m)

    @staticmethod
    def count_all(n: int) -> int:
        """
        Calculate the number of all possible combinations.
        :param n: The total number of elements,int.
        :return: The number of all possible combinations,int,if the number of combinations is greater than 2^63-1,return float("inf").
        """
        total_combinations = (1 << n) - 1
        if total_combinations > 2**63 - 1:
            return float("inf")
        return total_combinations

    def select(self, m: int) -> List[List[str]]:
        """
        Generate combinations with a specified number of elements.
        :param m: The number of elements in each combination,int.
        :return: A list of combinations,List[List[str]].
        """
        result = []
        self._select(0, [None] * m, 0, result)
        return result

    def select_all(self) -> List[List[str]]:
        """
        Generate all possible combinations of  selecting elements from the given data list,and it uses the select method.
        :return: A list of combinations,List[List[str]].
        """
        all_combinations = []
        for i in range(1, len(self.datas) + 1):
            all_combinations.extend(self.select(i))
        return all_combinations

    def _select(self, dataIndex: int, resultList: List[str], resultIndex: int, result: List[List[str]]):
        """
        Generate combinations with a specified number of elements by recursion.
        :param dataIndex: The index of the data to be selected,int.
        :param resultList: The list of elements in the combination,List[str].
        :param resultIndex: The index of the element in the combination,int.
        :param result: The list of combinations,List[List[str]].
        :return: None.
        """
        if resultIndex == len(resultList):
            result.append(resultList[:])
            return
        if dataIndex == len(self.datas):
            return
        resultList[resultIndex] = self.datas[dataIndex]
        self._select(dataIndex + 1, resultList, resultIndex + 1, result)
        self._select(dataIndex + 1, resultList, resultIndex, result)
