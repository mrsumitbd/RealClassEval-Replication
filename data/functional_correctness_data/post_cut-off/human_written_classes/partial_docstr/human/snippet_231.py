from dataclasses import dataclass

@dataclass
class HeavenStem:
    """天干"""
    name: str
    element: str
    yin_yang: int

    def __str__(self):
        return self.name

    def get_element(self):
        return self.element

    def get_yin_yang(self):
        return self.yin_yang

    def get_ten_star(self, other_stem: 'HeavenStem') -> str:
        """
        获取十神关系.
        """
        return self._calculate_ten_star(other_stem)

    def _calculate_ten_star(self, other: 'HeavenStem') -> str:
        """计算十神关系 - 使用专业数据"""
        from .professional_data import get_ten_gods_relation
        return get_ten_gods_relation(self.name, other.name)