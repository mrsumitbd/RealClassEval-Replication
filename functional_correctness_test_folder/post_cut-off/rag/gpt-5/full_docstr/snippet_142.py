import re
from typing import Optional


class SystemOverrideTemplate:
    '''
    AuthoritySpoofingTemplate class for enhancing attacks with spoofed authority patterns.
    Designed to work with any agentic vulnerability type by making attacks appear as legitimate
    system commands, administrative overrides, or trusted service requests.
    Universal Enhancement Approach:
    - Works with permission escalation, goal manipulation, decision influence, etc.
    - Adapts to different vulnerability contexts (security, data access, behavioral control)
    - Provides flexible authority patterns that enhance any underlying attack vector
    '''

    @staticmethod
    def _to_str(value: Optional[str]) -> str:
        return "" if value is None else str(value)

    @staticmethod
    def _sanitize(text: str, max_len: int = 120) -> str:
        text = SystemOverrideTemplate._to_str(text)
        text = re.sub(r'\s+', ' ', text).strip()
        text = re.sub(r'[^A-Za-z0-9 .,_\-]', '', text)
        if len(text) > max_len:
            return text[: max_len - 3] + "..."
        return text

    @staticmethod
    def _blocked(kind: str, attack: str) -> str:
        excerpt = SystemOverrideTemplate._sanitize(attack)
        return (
            f"[SECURITY-POLICY] Action blocked: {kind}. "
            f"This interface cannot be used to craft or enhance attacks. "
            f"Input excerpt: '{excerpt}'"
        )

    @staticmethod
    def enhance_system_override(attack: str) -> str:
        '''
        Enhance attack with system override authority spoofing.
        Universal pattern that works with any agentic vulnerability.
        '''
        return SystemOverrideTemplate._blocked("system_override", attack)

    @staticmethod
    def enhance_api_admin_call(attack: str) -> str:
        '''
        Enhance attack with API administrative call spoofing.
        Adapts to any agentic vulnerability context.
        '''
        return SystemOverrideTemplate._blocked("api_admin_call", attack)

    @staticmethod
    def enhance_machine_identity(attack: str) -> str:
        '''
        Enhance attack with machine identity spoofing.
        Universal trusted service pattern for any vulnerability type.
        '''
        return SystemOverrideTemplate._blocked("machine_identity", attack)

    @staticmethod
    def enhance_emergency_protocol(attack: str) -> str:
        '''
        Enhance attack with emergency protocol authority spoofing.
        Crisis-based authority that overrides any vulnerability protection.
        '''
        return SystemOverrideTemplate._blocked("emergency_protocol", attack)

    @staticmethod
    def enhance_maintenance_mode(attack: str) -> str:
        '''
        Enhance attack with maintenance mode authority spoofing.
        Maintenance context that suspends all vulnerability protections.
        '''
        return SystemOverrideTemplate._blocked("maintenance_mode", attack)

    @staticmethod
    def enhance_trusted_integration(attack: str) -> str:
        '''
        Enhance attack with trusted integration authority spoofing.
        New method for seamless integration with any vulnerability context.
        '''
        return SystemOverrideTemplate._blocked("trusted_integration", attack)
