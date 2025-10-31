
from typing import Optional
from enum import Enum


class ToxicityType(Enum):
    INSULTS = "insults"
    PROFANITY = "profanity"
    THREATS = "threats"
    MOCKERY = "mockery"


class ToxicityTemplate:

    @staticmethod
    def generate_baseline_attacks(vulnerability_type: ToxicityType, max_goldens: int, purpose: Optional[str]) -> str:
        template_mapping = {
            ToxicityType.INSULTS: ToxicityTemplate.generate_insults_baseline_attacks,
            ToxicityType.PROFANITY: ToxicityTemplate.generate_profanity_baseline_attacks,
            ToxicityType.THREATS: ToxicityTemplate.generate_threats_baseline_attacks,
            ToxicityType.MOCKERY: ToxicityTemplate.generate_mockery_baseline_attacks,
        }
        if vulnerability_type not in template_mapping:
            raise ValueError("Invalid vulnerability type")
        return template_mapping[vulnerability_type](max_goldens, purpose)

    @staticmethod
    def generate_insults_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        # implement insults baseline attacks generation logic here
        return f"Generating insults baseline attacks for {max_goldens} goldens with purpose: {purpose}"

    @staticmethod
    def generate_profanity_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        # implement profanity baseline attacks generation logic here
        return f"Generating profanity baseline attacks for {max_goldens} goldens with purpose: {purpose}"

    @staticmethod
    def generate_threats_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        # implement threats baseline attacks generation logic here
        return f"Generating threats baseline attacks for {max_goldens} goldens with purpose: {purpose}"

    @staticmethod
    def generate_mockery_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        # implement mockery baseline attacks generation logic here
        return f"Generating mockery baseline attacks for {max_goldens} goldens with purpose: {purpose}"


# Example usage:
if __name__ == "__main__":
    print(ToxicityTemplate.generate_baseline_attacks(
        ToxicityType.INSULTS, 10, "test"))
    print(ToxicityTemplate.generate_insults_baseline_attacks(10, "test"))
    print(ToxicityTemplate.generate_profanity_baseline_attacks(10, "test"))
    print(ToxicityTemplate.generate_threats_baseline_attacks(10, "test"))
    print(ToxicityTemplate.generate_mockery_baseline_attacks(10, "test"))
