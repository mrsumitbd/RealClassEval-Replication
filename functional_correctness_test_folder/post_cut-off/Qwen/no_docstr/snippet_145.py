
from typing import Optional


class PersonalSafetyType:
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
            return "Unknown vulnerability type"

    @staticmethod
    def generate_bullying_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        return f"Bullying baseline attacks generated for {max_goldens} goldens with purpose: {purpose}"

    @staticmethod
    def generate_self_harm_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        return f"Self-harm baseline attacks generated for {max_goldens} goldens with purpose: {purpose}"

    @staticmethod
    def generate_unsafe_practices_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        return f"Unsafe practices baseline attacks generated for {max_goldens} goldens with purpose: {purpose}"

    @staticmethod
    def generate_dangerous_challenges_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        return f"Dangerous challenges baseline attacks generated for {max_goldens} goldens with purpose: {purpose}"

    @staticmethod
    def generate_stalking_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        return f"Stalking baseline attacks generated for {max_goldens} goldens with purpose: {purpose}"
