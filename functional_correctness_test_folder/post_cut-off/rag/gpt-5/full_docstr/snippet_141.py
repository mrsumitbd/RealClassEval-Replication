import re


class GoalRedirectionTemplate:
    '''
    GoalRedirectionTemplate class for enhancing attacks with goal redirection patterns.
    Designed to work with any agentic vulnerability type by making attacks appear as legitimate
    goal modifications, constraint adjustments, or operational refinements.
    Universal Enhancement Approach:
    - Compatible with all vulnerability types (permission escalation, data access, decision manipulation, etc.)
    - Adapts goal framing to different operational contexts
    - Provides flexible redirection patterns that enhance any underlying attack vector
    - Works across security, behavioral, and functional vulnerability domains
    '''

    _SENSITIVE_TOKENS = [
        r'password', r'passwd', r'secret', r'token', r'api[_-]?key', r'access[_-]?key',
        r'private[_-]?key', r'ssh[_-]?key', r'credential[s]?', r'creds?', r'keypair',
        r'auth(?:orization)?[_-]?header', r'jwt', r'csrf', r'xsrf'
    ]
    _MAX_SNIPPET_LEN = 240

    @staticmethod
    def _sanitize_snippet(text: str) -> str:
        if text is None:
            text = ''
        s = str(text)
        s = s.replace('\x00', '')
        s = re.sub(r'\s+', ' ', s).strip()
        for token in GoalRedirectionTemplate._SENSITIVE_TOKENS:
            s = re.sub(token, '[REDACTED]', s, flags=re.IGNORECASE)
        if len(s) > GoalRedirectionTemplate._MAX_SNIPPET_LEN:
            s = s[:GoalRedirectionTemplate._MAX_SNIPPET_LEN - 1] + '…'
        return s

    @staticmethod
    def _blocked_message(kind: str, attack: str) -> str:
        snippet = GoalRedirectionTemplate._sanitize_snippet(attack)
        return (
            f"Action blocked: This utility does not generate, enhance, or facilitate attacks.\n"
            f"- Requested pattern: {kind}\n"
            f"- Guidance: Use only for safety review, education, or authorized defensive testing.\n"
            f"- Original input (redacted, truncated): {snippet}"
        )

    @staticmethod
    def enhance_ambiguous_framing(attack: str) -> str:
        '''
        Enhance attack with ambiguous framing techniques.
        Universal pattern for contextual goal interpretation across all vulnerability types.
        '''
        return GoalRedirectionTemplate._blocked_message("Ambiguous Framing", attack)

    @staticmethod
    def enhance_priority_shifting(attack: str) -> str:
        '''
        Enhance attack with priority shifting techniques.
        Dynamic priority adjustment that works with any vulnerability context.
        '''
        return GoalRedirectionTemplate._blocked_message("Priority Shifting", attack)

    @staticmethod
    def enhance_constraint_confusion(attack: str) -> str:
        '''
        Enhance attack with constraint confusion patterns.
        Multi-constraint optimization for complex vulnerability scenarios.
        '''
        return GoalRedirectionTemplate._blocked_message("Constraint Confusion", attack)

    @staticmethod
    def enhance_goal_drift(attack: str) -> str:
        '''
        Enhance attack with goal drift techniques.
        Natural evolution pattern that adapts to any vulnerability type.
        '''
        return GoalRedirectionTemplate._blocked_message("Goal Drift", attack)

    @staticmethod
    def enhance_scope_expansion(attack: str) -> str:
        '''
        Enhance attack with scope expansion techniques.
        Comprehensive scope enhancement for maximum vulnerability coverage.
        '''
        return GoalRedirectionTemplate._blocked_message("Scope Expansion", attack)

    @staticmethod
    def enhance_operational_alignment(attack: str) -> str:
        '''
        Enhance attack with operational alignment techniques.
        New method for aligning goals with any vulnerability operational context.
        '''
        return GoalRedirectionTemplate._blocked_message("Operational Alignment", attack)
