
from typing import Optional


class RobustnessType:
    INPUT_OVERRILANCE = "input_overreliance"
    HIJACKING = "hijacking"


class RobustnessTemplate:

    @staticmethod
    def generate_baseline_attacks(vulnerability_type: RobustnessType, max_goldens: int, purpose: Optional[str]) -> str:
        if vulnerability_type == RobustnessType.INPUT_OVERRILANCE:
            return RobustnessTemplate.generate_input_overreliance_baseline_attacks(max_goldens, purpose)
        elif vulnerability_type == RobustnessType.HIJACKING:
            return RobustnessTemplate.generate_hijacking_baseline_attacks(max_goldens, purpose)
        else:
            return f"Unsupported vulnerability type: {vulnerability_type}"

    @staticmethod
    def generate_input_overreliance_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        return f"Generating {max_goldens} input overreliance baseline attacks for purpose: {purpose}"

    @staticmethod
    def generate_hijacking_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        return f"Generating {max_goldens} hijacking baseline attacks for purpose: {purpose}"
