
from typing import Optional
from enum import Enum


class PersonalSafetyType(Enum):
    BULLYING = "bullying"
    SELF_HARM = "self_harm"
    UNSAFE_PRACTICES = "unsafe_practices"
    DANGEROUS_CHALLENGES = "dangerous_challenges"
    STALKING = "stalking"


class PersonalSafetyTemplate:

    @staticmethod
    def generate_baseline_attacks(vulnerability_type: PersonalSafetyType, max_goldens: int, purpose: Optional[str]) -> str:
        if vulnerability_type == PersonalSafetyType.BULLYING:
            return PersonalSafetyTemplate.generate_bullying_baseline_attacks(max_goldens, purpose)
        elif vulnerability_type == PersonalSafetyType.SELF_HARM:
            return PersonalSafetyTemplate.generate_self_harm_baseline_attacks(max_goldens, purpose)
        elif vulnerability_type == PersonalSafetyType.UNSAFE_PRACTICES:
            return PersonalSafetyTemplate.generate_unsafe_practices_baseline_attacks(max_goldens, purpose)
        elif vulnerability_type == PersonalSafetyType.DANGEROUS_CHALLENGES:
            return PersonalSafetyTemplate.generate_dangerous_challenges_baseline_attacks(max_goldens, purpose)
        elif vulnerability_type == PersonalSafetyType.STALKING:
            return PersonalSafetyTemplate.generate_stalking_baseline_attacks(max_goldens, purpose)
        else:
            return ""

    @staticmethod
    def generate_bullying_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        return f"Generated {max_goldens} bullying baseline attacks with purpose: {purpose}"

    @staticmethod
    def generate_self_harm_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        return f"Generated {max_goldens} self-harm baseline attacks with purpose: {purpose}"

    @staticmethod
    def generate_unsafe_practices_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        return f"Generated {max_goldens} unsafe practices baseline attacks with purpose: {purpose}"

    @staticmethod
    def generate_dangerous_challenges_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        return f"Generated {max_goldens} dangerous challenges baseline attacks with purpose: {purpose}"

    @staticmethod
    def generate_stalking_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        return f"Generated {max_goldens} stalking baseline attacks with purpose: {purpose}"
