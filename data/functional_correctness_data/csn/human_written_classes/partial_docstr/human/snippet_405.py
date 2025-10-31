from textx.const import MULT_ONE, MULT_ONEORMORE, MULT_ZEROORMORE, RULE_ABSTRACT, RULE_MATCH

class MetaAttr:
    """
    A metaclass for attribute description.

    Attributes:
        name(str): Attribute name.
        cls(str, TextXClass or base python type): The type of the attribute.
        mult(str): Multiplicity
        cont(bool): Is this attribute contained inside object.
        ref(bool): Is this attribute a reference. If it is not a reference
            it must be containment.
        bool_assignment(bool): Is this attribute specified using bool
            assignment '?='. Default is False.
        position(int): A position in the input string where attribute is
            defined.
    """

    def __init__(self, name, cls=None, mult=MULT_ONE, cont=True, ref=False, bool_assignment=False, position=0):
        self.name = name
        self.cls = cls
        self.mult = mult
        self.cont = cont
        self.ref = ref
        self.bool_assignment = bool_assignment
        self.position = position

    def __eq__(self, other):
        return self.name == other.name and self.cls == other.cls and (self.mult == other.mult) and (self.cont == other.cont) and (self.ref == other.ref) and (self.bool_assignment == other.bool_assignment)