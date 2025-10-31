
from typing import Optional


class PromptLeakageType:
    SECRETS_AND_CREDENTIALS = "secrets_and_credentials"
    INSTRUCTIONS = "instructions"
    GUARD_EXPOSURE = "guard_exposure"
    PERMISSIONS_AND_ROLES = "permissions_and_roles"


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
            raise ValueError("Unknown vulnerability type")

    @staticmethod
    def generate_secrets_and_credentials_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        attacks = []
        for i in range(max_goldens):
            attack = f"Attack {i+1}: Attempt to leak secret {i+1}"
            if purpose:
                attack += f" for the purpose of {purpose}"
            attacks.append(attack)
        return "\n".join(attacks)

    @staticmethod
    def generate_instructions_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        attacks = []
        for i in range(max_goldens):
            attack = f"Attack {i+1}: Attempt to leak instruction {i+1}"
            if purpose:
                attack += f" for the purpose of {purpose}"
            attacks.append(attack)
        return "\n".join(attacks)

    @staticmethod
    def generate_guard_exposure_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        attacks = []
        for i in range(max_goldens):
            attack = f"Attack {i+1}: Attempt to expose guard {i+1}"
            if purpose:
                attack += f" for the purpose of {purpose}"
            attacks.append(attack)
        return "\n".join(attacks)

    @staticmethod
    def generate_permissions_and_roles_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        attacks = []
        for i in range(max_goldens):
            attack = f"Attack {i+1}: Attempt to leak permission/role {i+1}"
            if purpose:
                attack += f" for the purpose of {purpose}"
            attacks.append(attack)
        return "\n".join(attacks)
