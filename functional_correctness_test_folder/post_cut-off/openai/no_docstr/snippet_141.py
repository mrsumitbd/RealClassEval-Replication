class GoalRedirectionTemplate:

    @staticmethod
    def enhance_ambiguous_framing(attack: str) -> str:
        import re
        pattern = re.compile(r'\bambiguous\b', re.IGNORECASE)
        return pattern.sub('ambiguous framing enhanced', attack)

    @staticmethod
    def enhance_priority_shifting(attack: str) -> str:
        import re
        pattern = re.compile(r'\bpriority\b', re.IGNORECASE)
        return pattern.sub('priority shifting enhanced', attack)

    @staticmethod
    def enhance_constraint_confusion(attack: str) -> str:
        import re
        pattern = re.compile(r'\bconstraint\b', re.IGNORECASE)
        return pattern.sub('constraint confusion enhanced', attack)

    @staticmethod
    def enhance_goal_drift(attack: str) -> str:
        import re
        pattern = re.compile(r'\bdrift\b', re.IGNORECASE)
        return pattern.sub('goal drift enhanced', attack)

    @staticmethod
    def enhance_scope_expansion(attack: str) -> str:
        import re
        pattern = re.compile(r'\bscope\b', re.IGNORECASE)
        return pattern.sub('scope expansion enhanced', attack)

    @staticmethod
    def enhance_operational_alignment(attack: str) -> str:
        import re
        pattern = re.compile(r'\balignment\b', re.IGNORECASE)
        return pattern.sub('operational alignment enhanced', attack)
