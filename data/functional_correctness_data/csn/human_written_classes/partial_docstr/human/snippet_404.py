class RuleCrossRef:
    """
    Used during meta-model parser construction for cross reference resolving
    of PEG rules, to support forward references.

    Attributes:
        rule_name(str): A name of the PEG rule that should be used to match
            this cross-ref. For link rule references it will be ID by default.
        cls(str or ClassCrossRef): Target class which is matched by the
            rule_name rule or which name is matched by the rule_name rule (for
            link rule references).
            Used for rule references in the RHS of the assignments to
            determine attribute type.
        position(int): A position in the input string of this cross-ref.
        rrel_tree: the RREL tree defined for this reference
    """

    def __init__(self, rule_name, cls, position, rrel_tree):
        self.rule_name = rule_name
        self.cls = cls
        self.position = position
        self.suppress = False
        self.scope_provider = None
        if rrel_tree is not None:
            from textx.scoping.rrel import create_rrel_scope_provider
            self.scope_provider = create_rrel_scope_provider(rrel_tree)

    def __str__(self):
        return self.rule_name