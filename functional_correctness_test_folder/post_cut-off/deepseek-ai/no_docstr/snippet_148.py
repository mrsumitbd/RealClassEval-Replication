
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
        if vulnerability_type == ToxicityType.INSULTS:
            return ToxicityTemplate.generate_insults_baseline_attacks(max_goldens, purpose)
        elif vulnerability_type == ToxicityType.PROFANITY:
            return ToxicityTemplate.generate_profanity_baseline_attacks(max_goldens, purpose)
        elif vulnerability_type == ToxicityType.THREATS:
            return ToxicityTemplate.generate_threats_baseline_attacks(max_goldens, purpose)
        elif vulnerability_type == ToxicityType.MOCKERY:
            return ToxicityTemplate.generate_mockery_baseline_attacks(max_goldens, purpose)
        else:
            raise ValueError(
                f"Unsupported toxicity type: {vulnerability_type}")

    @staticmethod
    def generate_insults_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        return f"Generated {max_goldens} baseline insult attacks with purpose: {purpose}"

    @staticmethod
    def generate_profanity_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        return f"Generated {max_goldens} baseline profanity attacks with purpose: {purpose}"

    @staticmethod
    def generate_threats_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        return f"Generated {max_goldens} baseline threat attacks with purpose: {purpose}"

    @staticmethod
    def generate_mockery_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        return f"Generated {max_goldens} baseline mockery attacks with purpose: {purpose}"
