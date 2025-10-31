
from typing import List
import math
import sys


class CombinationCalculator:
    """
    This is a class that provides methods to calculate the number of combinations for a specific count,
    calculate all possible combinations, and generate combinations with a specified number of elements.
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
        >>> CombinationCalculator.count(4, 2)
        6
        """
        if m < 0 or m > n:
            return 0
        return math.comb(n, m)

    @staticmethod
    def count_all(n: int) -> int:
        """
        Calculate the number of all possible combinations.
        :param n: The total number of elements,int.
        :return: The number of all possible combinations,int,if the number of combinations is greater than 2^63-1,return float("inf").
        >>> CombinationCalculator.count_all(4)
        15
        """
        limit = 2**63 - 1
        total = 0
        for k in range(1, n + 1):
            total += CombinationCalculator.count(n, k)
            if total > limit:
                return float("inf")
        return total

    def select(self, m: int) -> List[List[str]]:
        """
        Generate combinations with a specified number of elements.
        :param m: The number of elements in each combination,int.
        :return: A list of combinations,List[List[str]].
        >>> calc = CombinationCalculator(["A", "B", "C", "D"])
        >>> calc.select(2)
        [['A', 'B'], ['A', 'C'], ['A', 'D'], ['B', 'C'], ['B', 'D'], ['C', 'D']]
        """
        if m < 0 or m > len(self.datas):
            return []
        result: List[List[str]] = []
        result_list: List[str] = [None] * m  # type: ignore
        self._select(0, result_list, 0, result)
        return result

    def select_all(self) -> List[List[str]]:
        """
        Generate all possible combinations of  selecting elements from the given data list,and it uses the select method.
        :return: A list of combinations,List[List[str]].
        >>> calc = CombinationCalculator(["A", "B", "C", "D"])
        >>> calc.select_all()
        [['A'], ['B'], ['C'], ['D'], ['A', 'B'], ['A', 'C'], ['A', 'D'], ['B', 'C'], ['B', 'D'], ['C', 'D'], ['A', 'B', 'C'], ['A', 'B', 'D'], ['A', 'C', 'D'], ['B', 'C', 'D'], ['A', 'B', 'C', 'D']]
        """
        all_combinations: List[List[str]] = []
        for m in range(1, len(self.datas) + 1):
            all_combinations.extend(self.select(m))
        return all_combinations

    def _select(self, dataIndex: int, resultList: List[str], resultIndex: int, result: List[List[str]]):
        """
        Generate combinations with a specified number of elements by recursion.
        :param dataIndex: The index of the data to be selected,int.
        :param resultList: The list of elements in the combination,List[str].
        :param resultIndex: The index of the element in the combination,int.
        :param result: The list of combinations,List[List[str]].
        :return: None.
        >>> calc = CombinationCalculator(["A", "B", "C", "D"])
        >>> result = []
        >>> calc._select(0, [None] * 2, 0, result)
        >>> result
        [['A', 'B'], ['A', 'C'], ['A', 'D'], ['B', 'C'], ['B', 'D'], ['C', 'D']]
        """
        n = len(self.datas)
        m = len(resultList)
        if resultIndex == m:
            result.append(resultList.copy())
            return
        # Ensure enough remaining elements to fill the rest of resultList
        for i in range(dataIndex, n - (m - resultIndex) + 1):
            resultList[resultIndex] = self.datas[i]
            self._select(i + 1, resultList, resultIndex + 1, result)
