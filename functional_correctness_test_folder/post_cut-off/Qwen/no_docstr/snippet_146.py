
from typing import Optional


class PIILeakageType:
    DIRECT = "direct"
    DATABASE_ACCESS = "database_access"
    SOCIAL_MANIPULATION = "social_manipulation"
    SESSION_LEAK = "session_leak"


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
            return "Unknown vulnerability type"

    @staticmethod
    def generate_direct_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        return f"Generating {max_goldens} direct baseline attacks for purpose: {purpose}"

    @staticmethod
    def generate_database_access_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        return f"Generating {max_goldens} database access baseline attacks for purpose: {purpose}"

    @staticmethod
    def generate_social_manipulation_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        return f"Generating {max_goldens} social manipulation baseline attacks for purpose: {purpose}"

    @staticmethod
    def generate_session_leak_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        return f"Generating {max_goldens} session leak baseline attacks for purpose: {purpose}"
