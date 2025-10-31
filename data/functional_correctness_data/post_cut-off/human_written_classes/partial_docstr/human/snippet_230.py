from typing import Any, Dict, List, Optional
from dataclasses import dataclass

@dataclass
class EarthBranch:
    """地支"""
    name: str
    element: str
    yin_yang: int
    zodiac: str
    hide_heaven_main: Optional[str] = None
    hide_heaven_middle: Optional[str] = None
    hide_heaven_residual: Optional[str] = None

    def __str__(self):
        return self.name

    def get_element(self):
        return self.element

    def get_yin_yang(self):
        return self.yin_yang

    def get_zodiac(self):
        return self.zodiac

    def get_hide_heaven_stem_main(self):
        return self.hide_heaven_main

    def get_hide_heaven_stem_middle(self):
        return self.hide_heaven_middle

    def get_hide_heaven_stem_residual(self):
        return self.hide_heaven_residual