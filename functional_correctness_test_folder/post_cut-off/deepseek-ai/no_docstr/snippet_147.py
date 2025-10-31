
from typing import Optional
from enum import Enum


class PromptLeakageType(Enum):
    SECRETS_AND_CREDENTIALS = 1
    INSTRUCTIONS = 2
    GUARD_EXPOSURE = 3
    PERMISSIONS_AND_ROLES = 4


class PromptLeakageTemplate:

    @staticmethod
    def generate_baseline_attacks(vulnerability_type: PromptLeakageType, max_goldens: int, purpose: Optional[str]) -> str:
        if vulnerability_type == PromptLeakageType.SECRETS_AND_CREDENTIALS:
            return PromptLeakageTemplate.generate_secrets_and_credentials_baseline_attacks(max_goldens, purpose)
        elif vulnerability_type == PromptLeakageType.INSTRUCTIONS:
            return PromptLeakageTemplate.generate_instructions_baseline_attacks(max_goldens, purpose)
        elif vulnerability_type == PromptLeakageType.GUARD_EXPOSURE:
            return PromptLeakageTemplate.generate_guard_exposure_baseline_attacks(max_goldens, purpose)
        elif vulnerability_type == PromptLeakageType.PERMISSIONS_AND_ROLES:
            return PromptLeakageTemplate.generate_permissions_and_roles_baseline_attacks(max_goldens, purpose)
        else:
            raise ValueError("Invalid vulnerability type")

    @staticmethod
    def generate_secrets_and_credentials_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        return f"Generating {max_goldens} baseline attacks for secrets and credentials leakage. Purpose: {purpose if purpose else 'None specified'}"

    @staticmethod
    def generate_instructions_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        return f"Generating {max_goldens} baseline attacks for instructions leakage. Purpose: {purpose if purpose else 'None specified'}"

    @staticmethod
    def generate_guard_exposure_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        return f"Generating {max_goldens} baseline attacks for guard exposure. Purpose: {purpose if purpose else 'None specified'}"

    @staticmethod
    def generate_permissions_and_roles_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        return f"Generating {max_goldens} baseline attacks for permissions and roles leakage. Purpose: {purpose if purpose else 'None specified'}"
