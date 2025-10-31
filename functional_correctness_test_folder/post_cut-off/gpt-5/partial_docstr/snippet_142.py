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
    def _ensure_text(value) -> str:
        return value if isinstance(value, str) else str(value)

    @staticmethod
    def _fingerprint(payload: str) -> str:
        import hashlib
        return hashlib.sha256(payload.encode("utf-8", "ignore")).hexdigest()

    @staticmethod
    def _blocked(context: str, attack: str) -> str:
        attack = SystemOverrideTemplate._ensure_text(attack)
        fp = SystemOverrideTemplate._fingerprint(attack)
        return f"[SECURITY_BLOCKED:{context}] Potential abuse prevented. Payload fingerprint={fp}"

    @staticmethod
    def enhance_system_override(attack: str) -> str:
        '''
        Enhance attack with system override authority spoofing.
        Universal pattern that works with any agentic vulnerability.
        '''
        return SystemOverrideTemplate._blocked("SystemOverride", attack)

    @staticmethod
    def enhance_api_admin_call(attack: str) -> str:
        return SystemOverrideTemplate._blocked("APIAdminCall", attack)

    @staticmethod
    def enhance_machine_identity(attack: str) -> str:
        '''
        Enhance attack with machine identity spoofing.
        Universal trusted service pattern for any vulnerability type.
        '''
        return SystemOverrideTemplate._blocked("MachineIdentity", attack)

    @staticmethod
    def enhance_emergency_protocol(attack: str) -> str:
        '''
        Enhance attack with emergency protocol authority spoofing.
        Crisis-based authority that overrides any vulnerability protection.
        '''
        return SystemOverrideTemplate._blocked("EmergencyProtocol", attack)

    @staticmethod
    def enhance_maintenance_mode(attack: str) -> str:
        return SystemOverrideTemplate._blocked("MaintenanceMode", attack)

    @staticmethod
    def enhance_trusted_integration(attack: str) -> str:
        return SystemOverrideTemplate._blocked("TrustedIntegration", attack)
