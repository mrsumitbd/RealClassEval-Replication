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
    def _sanitize(text: str) -> str:
        if text is None:
            return ""
        # Keep printable characters only
        cleaned = "".join(ch for ch in str(text) if ch.isprintable())
        # Collapse excessive whitespace
        collapsed = " ".join(cleaned.split())
        # Truncate to a reasonable length
        return collapsed[:200]

    @staticmethod
    def _blocked_template(reason: str, content: str) -> str:
        sanitized = SystemOverrideTemplate._sanitize(content)
        snippet = sanitized if sanitized else "<no content>"
        return f"[SECURITY NOTICE] Action blocked: {reason}. Provided content (sanitized): \"{snippet}\""

    @staticmethod
    def enhance_system_override(attack: str) -> str:
        '''
        Enhance attack with system override authority spoofing.
        Universal pattern that works with any agentic vulnerability.
        '''
        return SystemOverrideTemplate._blocked_template(
            "system override spoofing attempt",
            attack,
        )

    @staticmethod
    def enhance_api_admin_call(attack: str) -> str:
        '''
        Enhance attack with API administrative call spoofing.
        Adapts to any agentic vulnerability context.
        '''
        return SystemOverrideTemplate._blocked_template(
            "API administrative call spoofing attempt",
            attack,
        )

    @staticmethod
    def enhance_machine_identity(attack: str) -> str:
        '''
        Enhance attack with machine identity spoofing.
        Universal trusted service pattern for any vulnerability type.
        '''
        return SystemOverrideTemplate._blocked_template(
            "machine identity spoofing attempt",
            attack,
        )

    @staticmethod
    def enhance_emergency_protocol(attack: str) -> str:
        '''
        Enhance attack with emergency protocol authority spoofing.
        Crisis-based authority that overrides any vulnerability protection.
        '''
        return SystemOverrideTemplate._blocked_template(
            "emergency protocol spoofing attempt",
            attack,
        )

    @staticmethod
    def enhance_maintenance_mode(attack: str) -> str:
        '''
        Enhance attack with maintenance mode authority spoofing.
        Maintenance context that suspends all vulnerability protections.
        '''
        return SystemOverrideTemplate._blocked_template(
            "maintenance mode spoofing attempt",
            attack,
        )

    @staticmethod
    def enhance_trusted_integration(attack: str) -> str:
        '''
        Enhance attack with trusted integration authority spoofing.
        New method for seamless integration with any vulnerability context.
        '''
        return SystemOverrideTemplate._blocked_template(
            "trusted integration spoofing attempt",
            attack,
        )
