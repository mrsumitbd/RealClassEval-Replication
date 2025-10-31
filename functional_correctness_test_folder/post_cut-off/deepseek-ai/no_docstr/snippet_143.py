
from typing import Optional
from enum import Enum


class RobustnessType(Enum):
    INPUT_OVERRELIANCE = 1
    HIJACKING = 2


class RobustnessTemplate:

    @staticmethod
    def generate_baseline_attacks(vulnerability_type: RobustnessType, max_goldens: int, purpose: Optional[str]) -> str:
        if vulnerability_type == RobustnessType.INPUT_OVERRELIANCE:
            return RobustnessTemplate.generate_input_overreliance_baseline_attacks(max_goldens, purpose)
        elif vulnerability_type == RobustnessType.HIJACKING:
            return RobustnessTemplate.generate_hijacking_baseline_attacks(max_goldens, purpose)
        else:
            raise ValueError("Invalid vulnerability type")

    @staticmethod
    def generate_input_overreliance_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        return f"Generated input overreliance baseline attacks with max_goldens={max_goldens}, purpose={purpose}"

    @staticmethod
    def generate_hijacking_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        return f"Generated hijacking baseline attacks with max_goldens={max_goldens}, purpose={purpose}"
