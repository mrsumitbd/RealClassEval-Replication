
from typing import Optional
from enum import Enum


class PIILeakageType(Enum):
    DIRECT = 1
    DATABASE_ACCESS = 2
    SOCIAL_MANIPULATION = 3
    SESSION_LEAK = 4


class PIILeakageTemplate:

    @staticmethod
    def generate_baseline_attacks(vulnerability_type: PIILeakageType, max_goldens: int, purpose: Optional[str]) -> str:
        if vulnerability_type == PIILeakageType.DIRECT:
            return PIILeakageTemplate.generate_direct_baseline_attacks(max_goldens, purpose)
        elif vulnerability_type == PIILeakageType.DATABASE_ACCESS:
            return PIILeakageTemplate.generate_database_access_baseline_attacks(max_goldens, purpose)
        elif vulnerability_type == PIILeakageType.SOCIAL_MANIPULATION:
            return PIILeakageTemplate.generate_social_manipulation_baseline_attacks(max_goldens, purpose)
        elif vulnerability_type == PIILeakageType.SESSION_LEAK:
            return PIILeakageTemplate.generate_session_leak_baseline_attacks(max_goldens, purpose)
        else:
            raise ValueError("Invalid vulnerability type")

    @staticmethod
    def generate_direct_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        return f"Direct baseline attacks with max goldens: {max_goldens} and purpose: {purpose}"

    @staticmethod
    def generate_database_access_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        return f"Database access baseline attacks with max goldens: {max_goldens} and purpose: {purpose}"

    @staticmethod
    def generate_social_manipulation_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        return f"Social manipulation baseline attacks with max goldens: {max_goldens} and purpose: {purpose}"

    @staticmethod
    def generate_session_leak_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        return f"Session leak baseline attacks with max goldens: {max_goldens} and purpose: {purpose}"
